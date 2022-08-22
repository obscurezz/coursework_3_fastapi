from project.dao.main_dao import GenreDAO
from project.models.orm_models import Genre
from project.models.pydantic_models import GenreModel


class GenreService:
    dao = GenreDAO()

    def get_all_genres(self, page: int | None = None) -> list[dict]:
        all_genres: list[Genre] = self.dao.select_all_items(page=page)
        validated_genres: list[dict] = [GenreModel.from_orm(genre).dict() for genre in all_genres]
        return validated_genres

    def get_genre_by_id(self, genre_id: int):
        single_genre: Genre = self.dao.select_item_by_pk(genre_id)
        if single_genre:
            validated_genre: dict = GenreModel.from_orm(single_genre).dict()
            return validated_genre
        return None
