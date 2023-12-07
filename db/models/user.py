from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from .common import DBCommon


class UserBase(SQLModel):
    name: str
    phone: str
    email: str
    unokod: str


class User(UserBase, DBCommon, table=True):
    __tablename__ = "users"


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class UserPatch(SQLModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    unokod: Optional[str] = None
