from fastapi import APIRouter, HTTPException, Query

from project.models.pydantic_models import DirectorModel
from project.services.directors_service import DirectorService

directors_router = APIRouter(prefix='/directors', tags=['directors'])
directors_service = DirectorService()


@directors_router.get('/', response_model=list[DirectorModel], status_code=200)
async def get_all_directors(page: int | None = Query(default=None)):
    if all_directors := directors_service.get_all_directors(page=page):
        return all_directors
    raise HTTPException(status_code=404, detail='No items found')


@directors_router.get('/{director_id}', response_model=DirectorModel, status_code=200)
async def get_single_director(director_id: int):
    if director := directors_service.get_director_by_id(director_id):
        return director
    raise HTTPException(status_code=404, detail=f'Director {director_id} not found')
