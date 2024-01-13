from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Relationship
from .common import DBTable
from git import TYPE_CHECKING

if TYPE_CHECKING:
    from .reservation import ReservationDB


class UserBase(SQLModel):
    name: str
    phone: str
    email: str
    unokod: str


class UserDB(UserBase, DBTable, table=True):
    __tablename__ = "users"

    reserved: Optional["ReservationDB"] = Relationship(back_populates="user")


class UserAdd(UserBase):
    pass


class User(UserBase):
    """
    Represents a user and a homeless
    """

    id: int


class UserUpdate(SQLModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    unokod: Optional[str] = None
