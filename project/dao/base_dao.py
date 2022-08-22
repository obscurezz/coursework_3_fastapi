from typing import Generic, TypeVar, Type, Optional

from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import IntegrityError, NoResultFound
from project.database.base_model import BaseORM
from project.database.db import engine
from project.app_settings import app_settings

T = TypeVar('T', bound=BaseORM)


class BaseDAO(Generic[T]):
    __model__: Type[BaseORM] = BaseORM
    session = Session(bind=engine)
    per_page = app_settings.ITEMS_PER_PAGE

    def select_all_items(self, page: int | None) -> list[Optional[T]]:
        query: Query = self.session.query(self.__model__)
        if page:
            selected_items: list[Optional[T]] = query.limit(self.per_page).offset((page - 1) * self.per_page)
        else:
            return query.all()

        if selected_items:
            return selected_items
        return []

    def select_item_by_pk(self, pk: int) -> Optional[T]:
        item: Optional[T] = self.session.query(self.__model__).get(pk)
        if item:
            return item
        return None

    def insert_item(self, **kwargs) -> Optional[T]:
        new_object: Optional[T] = self.__model__(**kwargs)

        self.session.add(new_object)
        try:
            self.session.commit()
            return new_object
        except (IntegrityError, NoResultFound):
            self.session.rollback()
            self.session.close()
            return None

    def update_item_by_pk(self, pk: int, **kwargs) -> Optional[T]:
        update_object: Optional[T] = self.session.query(self.__model__).get(pk)
        for k, v in kwargs.items():
            setattr(update_object, k, v)

        self.session.add(update_object)
        try:
            self.session.commit()
            return update_object
        except (IntegrityError, NoResultFound):
            self.session.rollback()
            self.session.close()
            return None

    def delete_item_by_pk(self, pk: int) -> Optional[T]:
        delete_item: Optional[T] = self.session.query(self.__model__).get(pk)

        self.session.delete(delete_item)
        try:
            self.session.commit()
            return delete_item
        except (IntegrityError, NoResultFound):
            self.session.rollback()
            self.session.close()
            return None
