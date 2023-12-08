from sqlmodel import SQLModel, Field
from .common import DBCommon


class Host(DBCommon, table=True):
    __tablename__ = "hosts"

    name: str
    address1: str
    address2: str
    count_of_available_places: int
    total_available_places: int
