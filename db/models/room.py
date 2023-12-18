from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .common import DBCommon
from .reservation import ReservationDB, Reservation_User


class RoomType(DBCommon, table=True):
    __table__ = "room_type"
    type_name: str

class RoomBase(SQLModel):
    name: str
    description: str
    nbr_of_beds: int
    room_type: RoomType

class HostDB(RoomBase, DBCommon, table=True):
    __tablename__ = "room"

    #reservations: List["ReservationDB"] = Relationship(back_populates="host")
