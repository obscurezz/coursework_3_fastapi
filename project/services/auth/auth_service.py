from pydantic import ValidationError, EmailStr
from sqlalchemy.exc import IntegrityError

from project.dao.main_dao import UserDAO
from project.models.pydantic_models import UserModel, ErrorModel
from project.tools.pass_tool import generate_password_hash


class AuthService:
    dao = UserDAO()

    def post_new_user(self, **kwargs):
        kwargs['password'] = generate_password_hash(kwargs.get('password'))
        new_user_model = UserModel(**kwargs)
        try:
            if self.dao.insert_item(**new_user_model.dict()):
                return new_user_model
            return None
        except ValidationError as ve:
            return ErrorModel(error='User validation error', message=str(ve))
        except IntegrityError as ie:
            return ErrorModel(error='User already exists', message=str(ie))

    def post_user_login(self, email: EmailStr, password: str):
        hashed_password = generate_password_hash(password)
        current_user = self.dao.select_user_by_email_and_password(email=email, hashed_password=hashed_password)
        if current_user:
            return UserModel.from_orm(current_user)
        return None
