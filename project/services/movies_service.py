from project.dao.main_dao import MovieDAO
from project.models.orm_models import Movie
from project.models.pydantic_models import MovieModel


class MovieService:
    dao = MovieDAO()

    def get_all_movies(self, page: int | None = None) -> list[dict]:
        all_movies: list[Movie] = self.dao.select_all_items(page=page)
        validated_movies: list[dict] = [MovieModel.from_orm(movie).dict() for movie in all_movies]
        return validated_movies

    def get_movie_by_id(self, movie_id: int):
        single_movie: Movie = self.dao.select_item_by_pk(movie_id)
        if single_movie:
            validated_movie: dict = MovieModel.from_orm(single_movie).dict()
            return validated_movie
        return None
