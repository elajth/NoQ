import os
from sqlalchemy import create_engine, Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from icecream import ic
from faker import Faker

# from core.config import settings
from db.models.user import User

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2:///noq")

ic(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=True)


def create_db_tables():
    # Create the table
    Base.metadata.create_all(bind=engine)


# Define a function to get a database session
def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def add_users():
    faker = Faker("sv_SE")
    session = get_session()

    for i in range(4):
        user = User(
            name=faker.first_name(),
            phone="0709-123123",
            email=faker.email(),
            unokod=""
        )
        session.add(user)
        session.commit()
        ic(user.id, user.name, "added")

    session.close()


if __name__ == "__main__":
    create_db_tables()
    add_users()
