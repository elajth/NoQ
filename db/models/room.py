from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .common import DBCommon
from git import TYPE_CHECKING

if TYPE_CHECKING:
    from .host import HostDB


class RoomBase(SQLModel):
    """
    A class to represent the rooms of the host
    """

    description: Optional[str] = None
    total_places: int
    host_id: int = Field(index=True, nullable=False, foreign_key="hosts.id")


class RoomDB(RoomBase, DBCommon, table=True):
    __tablename__ = "rooms"

    host: Optional["HostDB"] = Relationship(back_populates="rooms")


class Room(RoomBase):
    """
    A room at the host
    """

    id: int


class RoomAdd(RoomBase):
    pass
