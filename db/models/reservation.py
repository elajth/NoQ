from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from .common import DBModel


class Reservation(DBModel, table=True):
    __tablename__ = "reservation"

    startDateTime: datetime
    endDateTime: datetime
    host_id: int
    user_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
