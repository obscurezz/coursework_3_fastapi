from typing import Mapping

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from project.app_settings import app_settings
from project.models.pydantic_models import UserModel, PasswordModel
from project.services.auth.user_service import UserService

user_router = APIRouter(prefix='/user', tags=['user operations'])
user_service = UserService()

security = HTTPBearer()


@user_router.get('/me', response_model=UserModel, status_code=200)
async def get_user_info(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token: str = credentials.credentials
    try:
        payload: Mapping = jwt.decode(token, app_settings.authjwt_secret_key, algorithms=['HS256'])
        return user_service.get_user_by_credentials(email=payload.get('sub'))
    except jwt.exceptions.DecodeError as e:
        raise HTTPException(status_code=401, detail=str(e))


@user_router.put('/password', status_code=204)
async def put_user_new_password(password_request: PasswordModel,
                                credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, app_settings.authjwt_secret_key, algorithms=['HS256'])
        user_credentials = user_service.get_user_by_credentials(email=payload.get('sub'))
        return user_service.put_user_new_password(user_credentials.email,
                                                  old_password=password_request.old_password,
                                                  new_password=password_request.new_password)
    except jwt.exceptions.DecodeError as e:
        raise HTTPException(status_code=401, detail=str(e))
