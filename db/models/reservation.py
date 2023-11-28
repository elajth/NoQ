from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from .common import DBModel


class Reservation(DBModel, table=True):
    __tablename__ = "reservation"

    startDateTime: datetime
    endDateTime: datetime
    beds: int = Field(default=1, nullable=False, description="Antal bäddar")
    host_id: int
    user_id: int
