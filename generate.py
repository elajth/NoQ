import random
from sqlmodel import SQLModel, Session, create_engine, select
from sqlalchemy import func, table, column
from datetime import datetime, timedelta
from icecream import ic
from faker import Faker

from api.reservations import valid_reservation

from db.models.host import HostDB
from db.models.reservation import ReservationDB
from db.models.user import UserDB
from db.models.common import get_database_url

engine = create_engine(get_database_url(), echo=False)


def create_db_tables(drop_all: bool = False):
    if drop_all:
        SQLModel.metadata.drop_all(engine)
        ic("Drop all DB tables")
    # Create the table
    ic("Create DB tables")
    SQLModel.metadata.create_all(engine)


def table_count(table_name: str) -> int:
    """
    SELECT count("table_name".id)
    """
    my_table = table(table_name, column("id"))

    stmt = select(func.count()).select_from(my_table)

    with Session(engine) as session:
        try:
            count: int = session.exec(stmt).first()
            return count

        except Exception:
            return 0

    return 0


def count_records_in_database() -> str:
    reservations: int = table_count(ReservationDB.__tablename__)
    hosts: int = table_count(HostDB.__tablename__)
    users: int = table_count(UserDB.__tablename__)

    return f"<br/>hosts: {hosts}<br/>users: {users}<br/>reservations: {reservations}"


def get_session():
    with Session(engine) as session:
        return session


def add_hosts() -> int:
    faker = Faker("sv_SE")
    session = get_session()

    härbärge = [
        "Korskyrkan",
        "Grimmans Akutboende",
        "Bostället",
        "Stadsmissionen",
        "Ny gemenskap",
    ]

    print("\n---- HOSTS ----")

    for i in range(5):
        host = HostDB(
            id=i,
            name=härbärge[i],
            address1=faker.street_address(),
            address2=faker.postcode() + " " + faker.city(),
            count_of_available_places=i,
            total_available_places=i + 1,
        )

        with Session(engine) as session:
            session.add(host)
            session.commit()
            ic(host.id, host.name, "added")

    session.close()
    return i + 1


def add_reservation() -> int:
    session = get_session()
    i = 0
    while i < 20:
        reservation = ReservationDB(
            id=i,
            start_date=datetime.now() + timedelta(days=random.randint(1, 3)),
            end_date=datetime.now(),
            host_id=random.randint(0, 3),
            user_id=random.randint(0, 20),
        )
        with Session(engine) as session:
            if valid_reservation(reservation):
                session.add(reservation)
                session.commit()
                state = "Reservation added"
                i += 1
            else:
                state = "User already has a reservation this date"

            ic(reservation.user_id, reservation.start_date, state)

    session.close()
    return i


def add_users() -> int:
    faker = Faker("sv_SE")
    session = get_session()

    print("\n---- USERS ----")

    for i in range(20):
        namn = faker.name()
        user = UserDB(
            id=i,
            name=namn,
            phone="070" + f"{random.randint(0,9)}-{random.randint(121212,909090)}",
            email=namn.lower().replace(" ", ".") + "@hotmejl.se",
            unokod="",
        )
        with Session(engine) as session:
            session.add(user)
            session.commit()
            ic(user.id, user.name, "added")

    session.close()
    return i + 1


if __name__ == "__main__":
    create_db_tables(drop_all=True)
    add_hosts()
    add_users()
    add_reservation()
