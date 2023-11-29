from typing import Optional
from sqlmodel import Field, SQLModel
from icecream import ic


class DBModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)


def debug_connection(db_url: str):
    try:
        url = db_url.split(":")
        db_type = url[0]
        user = url[1]
        cloud_db = f'{db_type}://{url[2].split("@")[1]}'
        url = url[3].split("/")
        database = url[1].split("?")[0]
        ic(cloud_db, user, database)
        print("")  # formatting output
    except IndexError:
        print(db_url)