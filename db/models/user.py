from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Relationship
from .common import DBCommon
from git import TYPE_CHECKING

from .reservation import ReservationDB


class UserBase(SQLModel):
    name: str
    phone: str
    email: str
    unokod: str


class User(UserBase, DBCommon, table=True):
    __tablename__ = "users"

    reserved: Optional[ReservationDB] = Relationship(back_populates="user")


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class UserPatch(SQLModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    unokod: Optional[str] = None
