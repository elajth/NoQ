from typing import Optional, List
from fastapi import APIRouter
from sqlalchemy import func, and_
from sqlmodel import select, Session
from db.db_setup import get_db, get_session, engine
from db.models.reservation import Reservation
from db.models.host import Host

router = APIRouter()


@router.get("/reservations", response_model=List[Reservation])
async def get_reservations():
    with Session(engine) as session:
        reservation = session.exec(select(Reservation)).all()
        return reservation


# @router.get("/bookings", response_model=List[Reservation])
# async def get_bookings():
#     with Session(engine) as session:
#         reservation = session.exec(select(Reservation, Host).join(Host, isouter=False))
#         return reservation


# @router.post("/reservation")
# async def create_reservation(reservation: Reservation):
#     # reservations_list.append(reservation)
#     return True


# @router.get("/reservation/{id}")
# async def get_reservation(id: int):
#     # return {"reservation": reservations_list[id]}
#     return True


def validate_reservation(reservation: Reservation) -> bool:
    startdate = func.date(reservation.start_date)
    with get_session() as db:
        db_reservation = (
            db.query(Reservation)
            .filter(
                and_(
                    startdate == func.date(reservation.start_date),
                    Reservation.user_id == reservation.user_id,
                )
            )
            .first()
        )

    print(f"\nReservation.validate({reservation.start_date}, {reservation.user_id}):")

    # ic(reservation)

    return db_reservation is None