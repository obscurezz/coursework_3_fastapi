from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from project.database.db import engine
from project.models.orm_models import Director, Genre, Movie, User
from project.tools.utils import read_json_file, load_data
from project.tools.pass_tool import generate_password_hash


if __name__ == '__main__':
    data: dict[str, list[dict]] = read_json_file("fixtures.json")

    with Session(engine) as session:
        load_data(session, data['directors'], Director)
        load_data(session, data['genres'], Genre)
        load_data(session, data['movies'], Movie)

        for user in data['users']:
            user['password'] = generate_password_hash(user['password'])

        load_data(session, data['users'], User)
        try:
            session.commit()
        except IntegrityError as e:
            print(f'IntegrityError: {e.orig}')
        finally:
            session.close()
