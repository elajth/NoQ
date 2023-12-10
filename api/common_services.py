from typing import Optional, List
from fastapi import APIRouter, Depends

from sqlmodel import select, Session
from db.db_setup import get_db, engine
from db.models.host import HostDB

from generate import create_db_tables, add_hosts, add_reservation, add_users

router = APIRouter()


@router.get("/generate")
async def do_generate():
    try:
        create_db_tables(True)

        hosts = add_hosts()

        reservations = add_reservation()

        users = add_users()

        return {"hosts": hosts, "users": users, "reservations": reservations}

    except:
        return "Testdata finns redan."
