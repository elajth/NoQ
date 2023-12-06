from typing import Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field, select
# from sqlalchemy import and_, func
from .common import DBModel
# from db.db_setup import get_session
from icecream import ic

class Reservation(DBModel, table=True):
    __tablename__ = "reservation"

    start_date: date = Field(index=True, nullable=False)
    end_date: date
    host_id: int
    user_id: int = Field(index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)