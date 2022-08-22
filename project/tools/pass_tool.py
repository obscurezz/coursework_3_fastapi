import base64
import hashlib
import hmac
from typing import Union
from project.app_settings import app_settings


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name=app_settings.PWD_HASH_NAME,
        password=password.encode("utf-8"),
        salt=app_settings.PWD_SALT,
        iterations=100_000,
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compose_passwords(password_hash: Union[str, bytes], password: str) -> bool:
    decoded_digest: bytes = base64.b64decode(password_hash)

    hash_digest: bytes = __generate_password_digest(password)

    return hmac.compare_digest(decoded_digest, hash_digest)
