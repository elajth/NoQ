import os
from sqlalchemy import create_engine, Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from icecream import ic
from faker import Faker

# from core.config import settings
from db.models.user import User

from dotenv import load_dotenv
# Read settings from .env file
load_dotenv()

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2:///noq")

ic(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=True)


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
            name=faker.name(),
            phone="0709-123123",
            email=faker.email(),
            unokod=""
        )
        session.add(user)
        session.commit()
        ic(user.id, user.name, "added")

    session.close()


if __name__ == "__main__":
    
    add_users()
