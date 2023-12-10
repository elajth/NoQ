from typing import Optional
from datetime import datetime, date
from git import TYPE_CHECKING
from sqlmodel import SQLModel, Field, select, Relationship
from .common import DBCommon

if TYPE_CHECKING:
    from .user import User

if TYPE_CHECKING:
    from .host import HostDB


class ReservationBase(SQLModel):
    start_date: date = Field(index=True, nullable=False)
    user_id: int = Field(index=True, nullable=False)


class ReservationDB(DBCommon, table=True):
    __tablename__ = "reservations"

    start_date: date = Field(index=True, nullable=False)
    user_id: int = Field(index=True, nullable=False)

    host_id: int = Field(index=True, nullable=False, foreign_key="hosts.id")
    user_id: int = Field(index=True, nullable=False, foreign_key="users.id")

    host: Optional["HostDB"] = Relationship(back_populates="reservations")
    user: Optional["User"] = Relationship(back_populates="reserved")


class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: int


class ReservationDelete(SQLModel):
    id: int


class UserDetails(SQLModel):
    name: str
    reserved: Optional[ReservationDB] = Relationship(back_populates="user")


class ReservationWithUser(ReservationBase):
    id: int

    user: Optional[UserDetails] = None
