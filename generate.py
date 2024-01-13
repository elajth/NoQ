import random
from typing import List
from sqlmodel import SQLModel, Session, create_engine, select
from sqlalchemy import func, table, column
from datetime import datetime, timedelta
from icecream import ic
from faker import Faker

from api.reservations import valid_reservation

from db.models.reservation import ReservationDB
from db.models.host import HostDB
from db.models.user import UserDB
from db.models.room import RoomDB
from db.models.common import get_database_url


def create_db_tables(drop_all: bool = False):
    DATABASE_URL, DB_ECHO = get_database_url()

    if drop_all:
        # Set echo to True always when tables are dropped and created
        engine = create_engine(url=DATABASE_URL, echo=True)
        SQLModel.metadata.drop_all(engine)
        ic("Drop all DB tables")
        # Create the table
        SQLModel.metadata.create_all(engine)

    engine = create_engine(url=DATABASE_URL, echo=DB_ECHO)
    return engine


def table_count_rows(engine, table_name: str) -> int:
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


def count_records_in_database(engine) -> str:
    reservations: int = table_count_rows(engine, ReservationDB.__tablename__)
    hosts: int = table_count_rows(engine, HostDB.__tablename__)
    users: int = table_count_rows(engine, UserDB.__tablename__)

    return f"<br/>hosts: {hosts}<br/>users: {users}<br/>reservations: {reservations}"


def get_session(engine):
    with Session(engine) as session:
        return session


def set_testmode(test_engine):
    engine


def add_hosts(engine) -> int:
    faker = Faker("sv_SE")
    session = get_session(engine)

    härbärge = [
        "Korskyrkan",
        "Grimmans Akutboende",
        "Stadsmissionen",
        "Ny gemenskap",
        "Bostället",
    ]

    print("\n---- HOSTS ----")

    for i in range(5):
        host = HostDB(
            name=härbärge[i],
            address1=faker.street_address(),
            address2=faker.postcode() + " " + faker.city(),
            count_of_available_places=i * 2 + 1,
            total_available_places=i * 2 + 1,
        )

        with Session(engine) as session:
            session.add(host)
            session.commit()
            ic(host.id, host.name, "added")

    session.close()
    return i + 1


def get_host_id() -> int:
    with get_session(engine) as db:
        statement = select(HostDB)
        host: HostDB = db.exec(statement).first()

    if host is None:
        raise Exception("No host")

    return host.id


def get_user_id() -> int:
    with get_session(engine) as db:
        statement = select(UserDB)
        host: UserDB = db.exec(statement).first()

    if host is None:
        raise Exception("No UserDB")

    return host.id


def add_reservation(engine) -> int:
    print("\n---- RESERVATIONS ----")
    session = get_session(engine)
    i = 0
    host_min = get_host_id()
    user_min = get_user_id()

    while i < 20:
        reservation = ReservationDB(
            start_date=datetime.now() + timedelta(days=random.randint(1, 3)),
            end_date=datetime.now(),
            host_id=random.randint(host_min, host_min + 3),
            user_id=random.randint(user_min, user_min + 15),
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


def add_users(engine) -> int:
    session = get_session(engine)

    faker = Faker("sv_SE")

    print("\n---- USERS ----")

    for i in range(20):
        namn = faker.name()
        user = UserDB(
            # id=i,
            name=namn,
            phone="070" + f"{random.randint(0,9)}-{random.randint(121212,909090)}",
            email=namn.lower().replace(" ", ".") + "@hotmejl.se",
            unokod="1234",
        )
        with Session(engine) as session:
            session.no_autoflush
            session.add(user)
            session.commit()
            ic(user.id, user.name, "added")
            # session.merge(user)
            session.refresh(user)

    user = UserDB(
        # id=21,
        name="Andre",
        phone="070" + f"{random.randint(0,9)}-{random.randint(121212,909090)}",
        email="andre.ekespong" + "@hotmejl.se",
        unokod="1234",
    )
    with Session(engine) as session:
        session.no_autoflush
        session.add(user)
        session.commit()
        session.merge(user)
        session.refresh(user)
        session.commit()
        ic(user.id, user.name, "Andre added")

    session.close()
    return i + 1


def drop_all_tables_and_constraints(engine):
    """
    (On a live db) drops all foreign key constraints before dropping all tables.
    Workaround for SQLAlchemy not doing DROP ## CASCADE for drop_all()
    (https://github.com/pallets/flask-sqlalchemy/issues/722)
    """
    from sqlalchemy.engine.reflection import Inspector
    from sqlalchemy.schema import (
        DropConstraint,
        DropTable,
        MetaData,
        Table,
        ForeignKeyConstraint,
    )

    con = engine.connect()
    trans = con.begin()
    inspector = Inspector.from_engine(engine)

    # We need to re-create a minimal metadata with only the required things to
    # successfully emit drop constraints and tables commands for postgres (based
    # on the actual schema of the running instance)
    meta = MetaData()
    tables = []
    all_fkeys = []

    for table_name in inspector.get_table_names():
        fkeys = []

        for fkey in inspector.get_foreign_keys(table_name):
            if not fkey["name"]:
                continue

            fkeys.append(ForeignKeyConstraint((), (), name=fkey["name"]))

        tables.append(Table(table_name, meta, *fkeys))
        all_fkeys.extend(fkeys)

    for fkey in all_fkeys:
        con.execute(DropConstraint(fkey))

    for _table in tables:
        con.execute(DropTable(_table))

    trans.commit()


if __name__ == "__main__":
    # try:
    DATABASE_URL, DB_ECHO = get_database_url()
    ic(DATABASE_URL)
    engine = create_engine(url=DATABASE_URL, echo=DB_ECHO)

    # drop_all_tables_and_constraints(engine)
    # engine = create_db_tables(drop_all=True)
    add_hosts(engine)
    add_users(engine)
    add_reservation(engine)
    # except Exception as ex:
    # print("Exception: ", ex)
