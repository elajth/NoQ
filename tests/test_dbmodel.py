import sys
import os
from icecream import ic

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

# Add root directory to path to be able to find modules
project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root_dir)

from db.models.host import Host
from db.models.reservation import Reservation


from dotenv import load_dotenv

# Read settings from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///noq.sqlite")

engine = create_engine(DATABASE_URL, echo=True)


def get_host_reservations(id: int):
    with Session(engine) as session:
        statement = select(Host, Reservation).join(Reservation).where(Host.id == id)
        host = session.exec(statement).all()
        # Assuming host is a list of tuples or objects, convert it to a dictionary
        reservations_data = [
            {"host": h.Host.dict(), "reservation": h.Reservation.dict()} for h in host
        ]
        reservations_2 = [{"host": h.Host, "reservation": h.Reservation} for h in host]

        return reservations_data


def get_host(id: int):
    with Session(engine) as session:
        statement = select(Host, Reservation).join(Reservation).where(Host.id == id)
        host: Host = session.exec(statement).all()

        host.reservations = host.Reservation
        return host
        # Assuming host is a list of tuples or objects, convert it to a dictionary
        reservations_data = [
            {"host": host.Host.dict(), "reservation": host.Reservation.dict()}
        ]
        reservations_2 = [{"host": h.Host, "reservation": h.Reservation} for h in host]

        return reservations_data


def get_host_all(id: int):
    with Session(engine) as session:
        host = session.get(Host, id)

        statement = select(Reservation).where(Reservation.host_id == id)
        reservations_list: Host = session.exec(statement).all()

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
    test_host_reservations()
# [ic({"host": h['host'], "reservation": h['reservation']}) for h in host]
