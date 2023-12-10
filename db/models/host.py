from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from .common import DBCommon
from .reservation import Reservation


class HostBase(SQLModel):
    name: str
    address1: str
    address2: str
    count_of_available_places: int
    total_available_places: int


class Host(HostBase, table=True):
    __tablename__ = "hosts"

    id: Optional[int] = Field(default=None, primary_key=True)

    reservations: list["Reservation"] = Relationship(back_populates="host")


class HostRead(HostBase):
    id: int

class HostPatch(SQLModel):
    name: str
    address1: str
    address2: str
    count_of_available_places: int
    total_available_places: int
