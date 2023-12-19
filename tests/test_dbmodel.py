import pytest
import sys
import os
from faker import Faker
from icecream import ic
from sqlmodel import StaticPool

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

# Add root directory to path to be able to find modules
project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root_dir)

from db.models.host import HostDB
from db.models.reservation import ReservationDB
from db.models.room import RoomDB


from generate import add_hosts, add_reservation, add_users


def get_session(engine):
    """
    Returns an in memory database session
    """
    with Session(engine) as session:
        return session


def create_tables_add_content():
    # Use in memory database
    engine = create_engine(
        "sqlite:///",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True,
    )

    ic("create in memory database tables")

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    add_hosts(engine)
    add_users(engine)
    add_reservation(engine)
    return engine


def get_host_all(engine, id: int):
    with get_session(engine) as session:
        host = session.get(HostDB, id)

        statement = select(RoomDB).where(RoomDB.host_id == id)
        rooms_list: HostDB = session.exec(statement).all()

        host.rooms = rooms_list
        return host


def test_host_all():
    engine = create_tables_add_content()
    host = get_host_all(engine, 1)
    ic(host)
    assert host is not None


def get_host_reservations(engine, id: int):
    with get_session(engine) as session:
        statement = (
            select(HostDB, ReservationDB).join(ReservationDB).where(HostDB.id == id)
        )
        host = session.exec(statement).all()
        # Assuming host is a list of tuples or objects, convert it to a dictionary
        reservations_data = [
            {"host": h.HostDB.dict(), "reservation": h.ReservationDB.dict()}
            for h in host
        ]
        reservations_2 = [
            {"host": h.HostDB, "reservation": h.ReservationDB} for h in host
        ]

        return reservations_data


def get_host(engine, id: int):
    with get_session(engine) as session:
        statement = (
            select(HostDB, ReservationDB).join(ReservationDB).where(HostDB.id == id)
        )
        host: HostDB = session.exec(statement).all()

        host.reservations = host.Reservation
        return host
        # Assuming host is a list of tuples or objects, convert it to a dictionary
        reservations_data = [
            {"host": host.Host.dict(), "reservation": host.ReservationDB.dict()}
        ]
        reservations_2 = [
            {"host": h.Host, "reservation": h.ReservationDB} for h in host
        ]

        return reservations_data


def test_host_reservations():
    engine = create_tables_add_content()
    n: int = 0

    for reservation in get_host_reservations(engine, 1):
        n += 1

    assert n > 0


if __name__ == "__main__":
    test_host_all()
    # create_tables_add_content()
    # test_host_reservations()
# [ic({"host": h['host'], "reservation": h['reservation']}) for h in host]
