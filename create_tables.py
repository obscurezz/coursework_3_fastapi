from project.database.db import engine
from project.models import orm_models


if __name__ == '__main__':
    orm_models.BaseORM.metadata.create_all(bind=engine)
