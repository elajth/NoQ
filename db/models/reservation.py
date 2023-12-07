from typing import Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field, select
from .common import DBCommon


class Reservation(DBCommon, table=True):
    __tablename__ = "reservation"

    start_date: date = Field(index=True, nullable=False)
    end_date: date
    host_id: int
    user_id: int = Field(index=True, nullable=False)
