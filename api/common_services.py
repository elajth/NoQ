from typing import Optional, List
from fastapi import APIRouter, Depends

from sqlmodel import select, Session
from db.db_setup import get_db, engine
from db.models.host import Host

from generate import create_db_tables, add_hosts, add_reservation, add_users

router = APIRouter()

@router.get("/generate")
async def do_generate():
    try:
        create_db_tables(True)

        log = str(add_hosts()) + " hosts generated. "

        add_reservation
        log += str(add_reservation()) + " reservations generated. "

        log += str(add_users()) + " users generated. "
        return log

    except:
        return "Testdata finns redan."
