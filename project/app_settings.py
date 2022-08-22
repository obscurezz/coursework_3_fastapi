from datetime import timedelta
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'FastAPI coursework_3 Sky.pro'

    authjwt_secret_key: str = "m=+Y(L1!idBB"
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    access_expires: timedelta = timedelta(minutes=30)
    refresh_expires: timedelta = timedelta(days=30)

    PWD_SALT: bytes = b"ef64874e"
    PWD_HASH_NAME: str = "sha256"
    PWD_HASH_ITERATIONS: int = 100_000

    ITEMS_PER_PAGE: int = 12
    JSON_SORT_KEYS: bool = False
    JSON_AS_ASCII: bool = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sql_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


@lru_cache
def get_settings():
    return Settings()


app_settings = get_settings()
