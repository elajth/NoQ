import os
from icecream import ic
from sqlmodel import Session, create_engine
from dotenv import load_dotenv

# Read environment variables
DATABASE_URL = os.environ.get("DATABASE_URL", "")
DB_ECHO = os.environ.get("DB_ECHO", "")


if DATABASE_URL == "":
    # Read settings from .env file
    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///noq.sqlite")
    DB_ECHO = bool(os.getenv("DB_ECHO", "False").lower() == "true")

if "sqlite" in DATABASE_URL:
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

ic(DATABASE_URL, DB_ECHO)
engine = create_engine(
    DATABASE_URL, connect_args=connect_args, future=True, echo=DB_ECHO
)


def yield_session():
    """
    Yields a session
    """
    with Session(engine) as session:
        yield session


def get_session():
    """
    Returns a session
    """
    with Session(engine) as session:
        return session
