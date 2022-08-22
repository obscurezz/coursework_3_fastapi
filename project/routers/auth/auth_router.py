from typing import Union

from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT

from project.app_settings import app_settings
from project.models.pydantic_models import UserModel, UserLoginModel, ErrorModel, TokenModel
from project.services.auth.auth_service import AuthService

auth_router = APIRouter(prefix='/auth', tags=['authorization and login'])
auth_service = AuthService()


@auth_router.post('/register',
                  response_model=Union[UserModel, ErrorModel],
                  status_code=201)
async def register_new_user(new_user: UserModel | ErrorModel):
    new_user = auth_service.post_new_user(**new_user.dict())
    if new_user:
        return new_user
    raise HTTPException(status_code=400, detail='Something went wrong')


@auth_router.post('/login',
                  response_model=TokenModel,
                  status_code=200)
async def login_user(user: UserLoginModel, authorize: AuthJWT = Depends()):
    current_user = auth_service.post_user_login(user.email, user.password)
    if current_user:
        access_token = authorize.create_access_token(subject=current_user.email,
                                                     expires_time=app_settings.access_expires,
                                                     algorithm='HS256')
        refresh_token = authorize.create_refresh_token(subject=current_user.email,
                                                       expires_time=app_settings.refresh_expires,
                                                       algorithm='HS256')
        return TokenModel(access_token=access_token, refresh_token=refresh_token)
    raise HTTPException(status_code=401, detail='Incorrect email or password')


@auth_router.post('/refresh',
                  response_model=TokenModel,
                  status_code=200)
async def refresh_token(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user,
                                                     expires_time=app_settings.access_expires)
    new_refresh_token = authorize.create_refresh_token(subject=current_user,
                                                       expires_time=app_settings.refresh_expires)
    return TokenModel(access_token=new_access_token, refresh_token=new_refresh_token)
