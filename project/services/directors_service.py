from project.dao.main_dao import DirectorDAO
from project.models.orm_models import Director
from project.models.pydantic_models import DirectorModel


class DirectorService:
    dao = DirectorDAO()

    def get_all_directors(self, page: int | None = None):
        all_directors: list[Director] = self.dao.select_all_items(page=page)
        validated_directors: list[dict] = [DirectorModel.from_orm(director).dict() for director in all_directors]
        return validated_directors

    def get_director_by_id(self, director_id: int):
        single_director: Director = self.dao.select_item_by_pk(director_id)
        if single_director:
            validated_director: dict = DirectorModel.from_orm(single_director).dict()
            return validated_director
        return None
