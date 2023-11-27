import os
from sqlmodel import SQLModel, Session, create_engine
from datetime import datetime
from icecream import ic
from faker import Faker

from db.models.host import Host
from db.models.reservation import Reservation

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2:///noq")

ic(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=True)


def create_db_tables(drop_all: bool = False):
    if drop_all:
        SQLModel.metadata.drop_all(engine)
    # Create the table
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        return session


def add_hosts():
    faker = Faker("sv_SE")
    session = get_session()

    for i in range(2):
        host = Host(
            name=faker.company(),
            address1=faker.street_address(),
            address2=faker.postcode() + " " + faker.city(),
            count_of_available_places=20,
            total_available_places=25,
        )
        with Session(engine) as session:
            session.add(host)
            session.commit()
            ic(host.id, host.name, "added")

    session.close()


def add_reservation():
    faker = Faker("sv_SE")
    session = get_session()

    for i in range(2):
        reservation = Reservation(
            id=i,
            startDateTime=datetime.now(),
            endDateTime=datetime.now(),
            host_id=1 + i,
            user_id=2 + i,
        )
        with Session(engine) as session:
            session.add(reservation)
            session.commit()
            ic(reservation.id, "added")

    session.close()


if __name__ == "__main__":
    create_db_tables(drop_all=True)
    add_hosts()
    add_reservation()
