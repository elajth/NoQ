from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter

from sqlmodel import select, Session
from db.db_setup import get_db, engine
from db.models.reservation import Reservation

router = APIRouter()

reservations = []


@router.get("/reservations", response_model=List[Reservation])
async def get_reservations():
    with Session(engine) as session:
        hosts = session.exec(select(Reservation)).all()
        return hosts


@router.post("/reservations")
async def create_reservation(reservation: Reservation):
    reservations.append(reservation)
    return "Success"


@router.get("/reservations/{id}")
async def get_reservation(id: int):
    return {"reservation": reservations[id]}
