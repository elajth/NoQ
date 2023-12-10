from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .common import DBCommon
from .reservation import ReservationDB, Reservation, ReservationWithUser


class HostBase(SQLModel):
    name: str
    address1: str
    address2: str
    count_of_available_places: int
    total_available_places: int


class HostDB(HostBase, DBCommon, table=True):
    __tablename__ = "hosts"

    id: Optional[int] = Field(default=None, primary_key=True)

    reservations: List["ReservationDB"] = Relationship(back_populates="host")


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
    name: str
    address1: str
    address2: str
    count_of_available_places: int
    total_available_places: int


# Note: Without any back_populate makes it
# possible to retrieve a deep json-structure
class HostWithReservations(Host):
    """
    Host with a list of Reservation
    """

    reservations: List[ReservationWithUser] = []
