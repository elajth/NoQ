import os
import random
from sqlmodel import SQLModel, Session, create_engine
from datetime import datetime, timedelta
from icecream import ic
from faker import Faker

from api.reservations import validate_reservation

from db.models.host import Host
from db.models.reservation import Reservation
from db.models.common import get_database_url

engine = create_engine(get_database_url(), echo=False)


def create_db_tables(drop_all: bool = False):
    if drop_all:
        SQLModel.metadata.drop_all(engine)
    # Create the table
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        return session


def add_hosts() -> int:
    faker = Faker("sv_SE")
    session = get_session()

    härbärge = ["Korskyrkan", "Grimmans Akutboende", "Bostället", "Stadsmissionen"]

    for i in range(4):
        host = Host(
            id=i,
            name=härbärge[i],
            address1=faker.street_address(),
            address2=faker.postcode() + " " + faker.city(),
            count_of_available_places=12 + i * 3,
            total_available_places=15 + i * 4,
        )
        with Session(engine) as session:
            session.add(host)
            session.commit()
            ic(host.id, host.name, "added")

    session.close()
    return i


def add_reservation() -> int:
    faker = Faker("sv_SE")
    session = get_session()

    for i in range(9):
        reservation = Reservation(
            id=i,
            start_date=datetime.now() + timedelta(days=random.randint(1, 3)),
            end_date=datetime.now(),
            extra_info="Ove checkar",
            host_id=random.randint(0, 3),
            user_id=random.randint(1, 10),
        )
        with Session(engine) as session:
            if validate_reservation(reservation):
                session.add(reservation)
                session.commit()
                state = "Reservation added"
            else:
                state = "Not valid - User already has a reservation this date"

            ic(reservation.user_id, reservation.start_date, state)

    session.close()
    return i


if __name__ == "__main__":
    create_db_tables(drop_all=True)
    add_hosts()
    add_reservation()
