from typing import Optional
from datetime import datetime, date
from git import TYPE_CHECKING
from sqlmodel import SQLModel, Field, select, Relationship
from .common import DBCommon

if TYPE_CHECKING:
    from .host import Host


class ReservationBase(SQLModel):
    start_date: date = Field(index=True, nullable=False)
    user_id: int = Field(index=True, nullable=False)


class Reservation(DBCommon, table=True):
    __tablename__ = "reservations"

    start_date: date = Field(index=True, nullable=False)
    user_id: int = Field(index=True, nullable=False)

    host_id: int = Field(index=True, nullable=False, foreign_key="hosts.id")

    host: Optional["Host"] = Relationship(back_populates="reservations")


class ReservationCreate(ReservationBase):
    pass


class ReservationRead(ReservationBase):
    id: int


class ReservationDelete(SQLModel):
    id: int
