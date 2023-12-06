from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from .common import DBModel

class Host(DBModel, table=True):
    __tablename__ = "hosts"

    name: str
    address1: str
    address2: str
    count_of_available_places: int
    total_available_places: int
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)