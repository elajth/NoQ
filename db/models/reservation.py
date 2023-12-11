from typing import Optional
from datetime import datetime, date
from git import TYPE_CHECKING
from sqlmodel import SQLModel, Field, select, Relationship
from .common import DBCommon

class ReservationBase(SQLModel):
    start_date: date = Field(index=True, nullable=False)
    user_id: int = Field(index=True, nullable=False)
    host_id: int = Field(index=True, nullable=False)


class ReservationDB(DBCommon, table=True):
    __tablename__ = "reservations"

    start_date: date = Field(index=True, nullable=False)
    
    host_id: int = Field(index=True, nullable=False, foreign_key="hosts.id")
    user_id: int = Field(index=True, nullable=False, foreign_key="users.id")

    host: Optional["HostDB"] = Relationship(back_populates="reservations")
    user: Optional["UserDB"] = Relationship(back_populates="reserved")


class ReservationAdd(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: int


class ReservationDelete(SQLModel):
    id: int


class User(SQLModel):
    id: int
    name: str
    reserved: Optional[ReservationDB] = Relationship(back_populates="user")


class Host(SQLModel):
    id: int
    name: str
    reservations: Optional[ReservationDB] = Relationship(back_populates="host")


class Reservation_User(SQLModel):
    id: int
    start_date: date

    user: Optional[User] = None


class Reservation_User_Host(SQLModel):
    id: int
    start_date: date

    user: Optional[User] = None
    host: Optional[Host] = None
