import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from icecream import ic

from dotenv import load_dotenv
# Read settings from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///noq.sqlite")
engine = create_engine(
    DATABASE_URL, connect_args={}, future=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)

Base = declarative_base()

# DB utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session