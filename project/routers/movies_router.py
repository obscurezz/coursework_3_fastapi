from fastapi import APIRouter, Query, HTTPException

from project.services.movies_service import MovieService
from project.models.pydantic_models import MovieModel

movies_router = APIRouter(prefix='/movies', tags=['movies'])
movies_service = MovieService()


@movies_router.get('/', response_model=list[MovieModel], status_code=200)
async def get_all_movies(page: int | None = Query(default=None)):
    if all_movies := movies_service.get_all_movies(page=page):
        return all_movies
    raise HTTPException(status_code=404, detail='No items found')


@movies_router.get('/{movie_id}', response_model=MovieModel, status_code=200)
async def get_single_movie(movie_id: int):
    if movie := movies_service.get_movie_by_id(movie_id):
        return movie
    raise HTTPException(status_code=404, detail=f'Movie {movie_id} not found')
