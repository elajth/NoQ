from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func, and_
from sqlmodel import select, Session
from db.db_setup import yield_session, get_session, engine
from db.models.reservation import (
    ReservationDB,
    Reservation,
    Reservation_User,
    Reservation_User_Host,
    ReservationAdd,
)
from db.models.host import HostDB
from icecream import ic

router = APIRouter()


@router.get("/reservations", response_model=List[Reservation_User])
async def get_reservations(*, session: Session = Depends(yield_session)):
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


@router.post("/reservations", response_model=ReservationDB)
async def add_reservation(
    *, session: Session = Depends(yield_session), reservation: ReservationAdd
):
    # TODO: Byt till ReservationDB.model_validate(team) vid ny version av SQLModel
    rsrv: ReservationDB = ReservationDB.from_orm(reservation)

    if not valid_reservation(rsrv):
        raise HTTPException(
            status_code=400,  # https://docs.oracle.com/en/cloud/saas/marketing/eloqua-develop/Developers/GettingStarted/APIRequests/Validation-errors.htm
            detail="Dubbelbokning samma dag för denna brukare",
            headers={"Error": "UniquenessRequirement", "Msg": "User is booked already"},
        )

    elif not place_available(rsrv):
        raise HTTPException(
            status_code=400,
            detail="No available places",
            headers={"Error": "UniquenessRequirement", "Msg": "No available places"},
        )

    else:
        with Session(engine) as session:
            session.add(rsrv)
            session.commit()
            session.refresh(rsrv)
            ic("RESERVATION ADDED")
    return rsrv


@router.get("/reservations/{id}", response_model=Reservation_User)
async def get_reservation(*, id: int, session: Session = Depends(yield_session)):
    reservation = session.get(ReservationDB, id)

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


def valid_reservation(reservation: ReservationDB) -> bool:
    startdate = func.date(reservation.start_date)
    with get_session() as db:
        statement = (
            select(ReservationDB)
            .where(ReservationDB.start_date == startdate)
            .where(ReservationDB.user_id == reservation.user_id)
        )
        existing_reservation: Reservation = db.execute(statement).first()

    if existing_reservation is not None:
        ic("Dubbelbokning")
        ic(existing_reservation)
        return False

    return True


def place_available(reservation: ReservationDB):
    host_id = reservation.host_id
    with get_session() as db:
        statement = (
            select(HostDB.total_available_places)
            .where(HostDB.id == host_id)
        )
        total_places: Reservation = db.execute(statement).first()
        ic(total_places)

    with get_session() as db:
        statement = (
            select(func.count(ReservationDB.id))
            .where(ReservationDB.host_id == host_id)
        )
        reservations: Reservation = db.execute(statement).one()
        ic(reservations)

    if total_places[0] <= reservations[0]:
        ic("No available places")
        ic("Places:", total_places, "Reservations:", reservations)
        return False

    return True
