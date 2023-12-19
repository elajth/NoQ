from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .common import DBCommon
from git import TYPE_CHECKING

if TYPE_CHECKING:
    from .room import RoomDB


class HostBase(SQLModel):
    name: str
    address1: str
    address2: str
    count_of_available_places: int
    total_available_places: int


class HostDB(HostBase, DBCommon, table=True):
    __tablename__ = "hosts"

    id: Optional[int] = Field(default=None, primary_key=True)

    rooms: List["RoomDB"] = Relationship(back_populates="host")


class Host(HostBase):
    """
    Härbärge
    """

    id: int


class HostAdd(HostBase):
    """
    Lägg till härbärge
    """

    pass


class HostUpdate(SQLModel):
    name: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    count_of_available_places: Optional[int] = None
    total_available_places: Optional[int] = None


# Note: Without any back_populate makes it
# possible to retrieve a deep json-structure
class Host_Rooms(Host):
    """
    Host with a list of Reservation
    """

    rooms: List["Room"] = []
