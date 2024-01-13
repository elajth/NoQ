from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from .common import DBTable, DBCommon
from git import TYPE_CHECKING

from .user import User
from .host import Host


class ReservationBase(SQLModel):
    start_date: date = Field(index=True, nullable=False)
    user_id: int = Field(index=True, nullable=False)
    host_id: int = Field(index=True, nullable=False)


class ReservationDB(DBCommon, table=True):
    __tablename__ = "reservations"

    start_date: date = Field(index=True, nullable=False)

    host_id: int = Field(index=True, nullable=False, foreign_key="hosts.id")
    user_id: int = Field(index=True, nullable=False, foreign_key="users.id")

    # host: Optional["HostDB"] = Relationship(back_populates="reservations")
    user: Optional["UserDB"] = Relationship(back_populates="reserved")


class ReservationAdd(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: int


class ReservationDelete(SQLModel):
    id: int


class Reservation_User(Reservation):
    user: User


class Reservation_User_Host(Reservation):
    user: User
    host: Host
