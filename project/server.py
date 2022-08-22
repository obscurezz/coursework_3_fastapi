from fastapi import FastAPI, Request
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from redis import Redis
from starlette.responses import JSONResponse

from project.app_settings import app_settings
from project.routers.auth.auth_router import auth_router
from project.routers.auth.user_router import user_router
from project.routers.directors_router import directors_router
from project.routers.genres_router import genres_router
from project.routers.movies_router import movies_router


def create_app() -> FastAPI:
    app = FastAPI()
    redis_conn = Redis(host='localhost', port=6379, db=0, decode_responses=True)

    @app.exception_handler(AuthJWTException)
    def authjwt_exception_handler(request: Request, exc: AuthJWTException()):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )

    @AuthJWT.load_config
    def get_config():
        return app_settings

    @AuthJWT.token_in_denylist_loader
    def check_if_token_in_denylist(decrypted_token):
        jti = decrypted_token['jti']
        entry = redis_conn.get(jti)
        return entry and entry == 'true'

    app.include_router(genres_router)
    app.include_router(movies_router)
    app.include_router(directors_router)
    app.include_router(auth_router)
    app.include_router(user_router)
    return app
