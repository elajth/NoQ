from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from icecream import ic
from sqlmodel import select, Session
from db.db_setup import get_db, engine
from db.models.host import HostDB, Host, Host_Reservations
from db.models.reservation import ReservationDB

from generate import create_db_tables, add_hosts, add_reservation, add_users

router = APIRouter()


@router.get("/hosts", response_model=List[Host])
async def list_hosts(skip: int = 0, limit: int = 100):
    with Session(engine) as session:
        hosts = session.exec(select(HostDB)).all()
        return hosts


# @router.post("/hosts")
# async def create_host(host: Host):
#     # hosts.append(host)
#     return "Success"


@router.get("/hosts/{id}", response_model=Host_Reservations)
async def get_host(*, id: int, session: Session = Depends(get_db)):
    host = session.get(HostDB, id)

    if not host:
        raise HTTPException(status_code=404, detail="Host not found")
    return host
