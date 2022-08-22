from fastapi import APIRouter, Query, HTTPException

from project.models.pydantic_models import GenreModel
from project.services.genres_service import GenreService

genres_router = APIRouter(prefix='/genres', tags=['genres'])
genres_service = GenreService()


@genres_router.get('/', response_model=list[GenreModel], status_code=200)
async def get_all_genres(page: int | None = Query(default=None)):
    if all_genre := genres_service.get_all_genres(page=page):
        return all_genre
    raise HTTPException(status_code=404, detail='No items found')


@genres_router.get('/{genre_id}', response_model=GenreModel, status_code=200)
async def get_single_genre(genre_id: int):
    if genre := genres_service.get_genre_by_id(genre_id):
        return genre
    raise HTTPException(status_code=404, detail=f'Genre {genre_id} not found')
