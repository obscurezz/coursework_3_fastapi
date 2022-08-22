from typing import Type

from pydantic import EmailStr

from project.dao.base_dao import BaseDAO
from project.models.orm_models import Movie, Genre, Director, User, UserFavorites


class MovieDAO(BaseDAO[Movie]):
    __model__: Type[Movie] = Movie


class GenreDAO(BaseDAO[Genre]):
    __model__: Type[Genre] = Genre


class DirectorDAO(BaseDAO[Director]):
    __model__: Type[Director] = Director


class UserDAO(BaseDAO[User]):
    __model__: Type[User] = User

    def select_user_by_email_and_password(self, email: EmailStr, hashed_password: str | None = None) -> User | None:
        if hashed_password:
            user: User = self.session.query(self.__model__).filter_by(email=email, password=hashed_password).one()
        else:
            user: User = self.session.query(self.__model__).filter_by(email=email).one()
        if user:
            return user
        return None


class UserFavoritesDAO(BaseDAO[UserFavorites]):
    __model__: Type[UserFavorites] = UserFavorites
