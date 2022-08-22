from pydantic import EmailStr

from project.dao.main_dao import UserDAO
from project.models.orm_models import User
from project.models.pydantic_models import UserModel
from project.tools.pass_tool import generate_password_hash, compose_passwords


class UserService:
    dao = UserDAO()

    def get_user_by_credentials(self, email: EmailStr):
        current_user: User = self.dao.select_user_by_email_and_password(email=email)
        if current_user:
            return UserModel.from_orm(current_user)
        return None

    def put_user_new_password(self, email: EmailStr, old_password: str, new_password: str):
        current_user: UserModel = self.get_user_by_credentials(email=email)
        if compose_passwords(current_user.password, old_password):
            new_hash_password = generate_password_hash(new_password)
            return self.dao.update_item_by_pk(current_user.id, password=new_hash_password)
        return None
