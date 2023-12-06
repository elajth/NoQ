from datetime import datetime
from sqlmodel import SQLModel, Field
from .common import DBModel

class User(DBModel, table=True):
    __tablename__ = "users"

    name: str
    phone: str
    email: str
    unokod: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)