import sys
import os
from icecream import ic

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

# Add root directory to path to be able to find modules
project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root_dir)

from db.models.host import HostDB
from db.models.reservation import ReservationDB
from db.models.user import UserDB
from generate import add_hosts, add_reservation, add_users

from dotenv import load_dotenv

# Read settings from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///noq.sqlite")

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    add_hosts()
    add_users()
    add_reservation()


def get_host_reservations(id: int):
    with Session(engine) as session:
        statement = (
            select(HostDB, ReservationDB).join(ReservationDB).where(HostDB.id == id)
        )
        host = session.exec(statement).all()
        # Assuming host is a list of tuples or objects, convert it to a dictionary
        reservations_data = [
            {"host": h.HostDB.model_dump(), "reservation": h.ReservationDB.model_dump()}
            for h in host
        ]

        return reservations_data


def get_host(id: int):
    with Session(engine) as session:
        statement = (
            select(HostDB, ReservationDB).join(ReservationDB).where(HostDB.id == id)
        )
        host: HostDB = session.exec(statement).all()

        host.reservations = host.Reservation
        return host
        # Assuming host is a list of tuples or objects, convert it to a dictionary
        reservations_data = [
            {
                "host": host.Host.model_dump(),
                "reservation": host.ReservationDB.model_dump(),
            }
        ]
        reservations_2 = [
            {"host": h.Host, "reservation": h.ReservationDB} for h in host
        ]

        return reservations_data


def get_host_all(id: int):
    with Session(engine) as session:
        host = session.get(HostDB, id)

        statement = select(ReservationDB).where(ReservationDB.host_id == id)
        reservations_list: HostDB = session.exec(statement).all()

        host.reservations = reservations_list
        return host


def test_host_all():
    assert get_host_all(1) is not None


def test_host_reservations():
    n: int = 0

    for host in get_host_reservations(1):
        n += 1
        ic(host)

    assert n > 0
    print(n)


if __name__ == "__main__":
    create_db_and_tables()
    test_host_reservations()
# [ic({"host": h['host'], "reservation": h['reservation']}) for h in host]
