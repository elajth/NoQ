import os
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import DateTime, func, Column
from icecream import ic
from dotenv import load_dotenv


class DBCommon(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default=None, nullable=True)


def get_database_url():
    # Read settings from .env file
    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///noq.sqlite")
    debug_connection(DATABASE_URL)
    return DATABASE_URL


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


def print_code(filename: str, from_line: int, to_line: int):
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as file:
            data = file.read().split("\n")
            for i in range(from_line - 1, to_line):
                print(data[i])
