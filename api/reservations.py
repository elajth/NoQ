from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func, and_
from sqlmodel import select, Session
from db.db_setup import get_db, get_session, engine
from db.models.reservation import (
    ReservationDB,
    Reservation,
    Reservation_User,
    ReservationAdd,
)
from db.models.host import HostDB
from icecream import ic

router = APIRouter()


@router.get("/reservations", response_model=List[Reservation])
async def get_reservations():
    with Session(engine) as session:
        reservation = session.exec(select(ReservationDB)).all()
        return reservation


# @router.get("/reservations", response_model=List[Reservation])
# async def get_reservations():
#     with Session(engine) as session:
#         reservation = session.exec(select(Reservation, Host).join(Host, isouter=False))
#         return reservation


# @router.post("/reservations")
# async def create_reservation(reservation: Reservation):
#     # reservations_list.append(reservation)
#     return True


@router.post("/reservations", response_model=ReservationAdd)
async def add_reservation(reservation: ReservationAdd):
    _reservation: ReservationDB = ReservationDB.from_orm(reservation)
    ic(_reservation)
    if not valid_reservation(_reservation):
        raise HTTPException(
            status_code=404, detail="Dubbelbokning samma dag för denna brukare"
        )

    with Session(engine) as session:
        session.add(_reservation)
        session.commit()
        session.refresh(_reservation)
    return _reservation


@router.get("/reservations/{id}", response_model=Reservation_User)
async def get_reservation(*, id: int, session: Session = Depends(get_db)):
    reservation = session.get(ReservationDB, id)

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


def valid_reservation(reservation: ReservationDB) -> bool:
    startdate = func.date(reservation.start_date)
    with get_session() as db:
        db_reservation = (
            db.query(ReservationDB)
            .filter(
                and_(
                    startdate == func.date(reservation.start_date),
                    ReservationDB.user_id == reservation.user_id,
                )
            )
            .first()
        )

    ic(reservation)

    # ic(reservation)

    return db_reservation is None
