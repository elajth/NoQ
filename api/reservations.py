from typing import Optional, List
import fastapi
from datetime import datetime
from pydantic import BaseModel

router = fastapi.APIRouter()

reservations = []

class Reservation(BaseModel):
    id: int
    startDateTime: datetime
    endDateTime: datetime
    host_id: int
    user_id: int

@router.get("/reservations", response_model=List[Reservation])
async def get_reservations():
    return reservations


@router.post("/reservations")
async def create_reservation(reservation: Reservation):
    reservations.append(reservation)
    return "Success"

@router.get("/reservations/{id}")
async def get_reservation(id: int):
    return { "reservation": reservations[id] }