import json
from typing import Type
from sqlalchemy.orm import Session

from project.database.base_model import BaseORM


def read_json_file(filename: str, encoding: str = 'utf-8') -> list | dict:
    with open(filename, encoding=encoding) as jsonfile:
        return json.load(jsonfile)


def load_data(db: Session, data: list[dict], model: Type[BaseORM]):
    for item in data:
        item['id'] = item.pop('pk')
        db.add(model(**item))
