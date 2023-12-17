from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .common import DBCommon
from .host import HostDB

class RoomBase(SQLModel):
    """
    A class to represent the rooms of the host
    """
    description: Optional[str] = None
    total_places: int
    host_id: int = Field(index=True, nullable=False)

class RoomDB(RoomBase, DBCommon, table=True):
    __tablename__ = "rooms"
    id: Optional[int] = Field(default=None, primary_key=True)
    # beds = List["BedDB"] = Relationship(back_populates="beds")

class RoomAdd(RoomBase):
    pass
