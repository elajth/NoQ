from typing import Optional, List
from fastapi import APIRouter, Depends

from sqlmodel import select, Session
from db.db_setup import get_db, engine
from db.models.host import Host

from generate_sqlmodel import create_db_tables, add_hosts, add_reservation
from generate import add_users

router = APIRouter()


@router.get("/host", response_model=List[Host])
async def get_hosts(skip: int = 0, limit: int = 100):
    with Session(engine) as session:
        hosts = session.exec(select(Host)).all()
        return hosts


# @router.post("/hosts")
# async def create_host(host: Host):
#     # hosts.append(host)
#     return "Success"


# @router.get("/hosts/{id}")
# async def get_host(id: int):
#     return {"host": "not implemented"}


@router.get("/generate")
async def do_generate():
    try:
        create_db_tables(True)

        log = str(add_hosts()) + " hosts generated. "

        add_reservation
        log += str(add_reservation()) + " reservations generated. "

        log += str(add_users()) + " users  generated. "
        return log

    except:
        return "Testdata finns redan."
