from typing import List
from fastapi import APIRouter, HTTPException, Depends
from icecream import ic
from sqlmodel import select, Session
from sqlalchemy import func
from db.db_setup import yield_session, get_session, engine
from db.models.reservation import (
    ReservationDB,
    Reservation,
    Reservation_User,
    ReservationAdd,
    Host_Reservation,
)
from db.models.host import HostDB

router = APIRouter()


@router.get("/reservations", response_model=List[Reservation_User])
async def list_reservations(
    *,
    session: Session = Depends(yield_session),
    # start_date: Date = "2022-01-01",
    skip: int = 0,
    limit: int = 100
):
    reservation = session.exec(
        select(ReservationDB)
        .offset(skip)
        .limit(limit)
        .order_by(ReservationDB.start_date)
    ).all()
    return reservation


@router.post("/reservations", response_model=Reservation)
async def add_reservation(
    *, session: Session = Depends(yield_session), reservation: ReservationAdd
):
    # TODO: Byt till ReservationDB.model_validate(team)
    # vid ny version av SQLModel
    rsrv: ReservationDB = ReservationDB.from_orm(reservation)

    if reservation.user_id < 1:
        ic(reservation)
        # https://docs.oracle.com/en/cloud/saas/marketing/eloqua-develop/Developers/GettingStarted/APIRequests/Validation-errors.htm
        raise HTTPException(
            status_code=400,
            detail="Error: user_id = 0",
            headers={"Error": "EndpointParameterError", "Msg": "user_id = 0"},
        )

    if reservation.host_id < 1:
        ic(reservation)
        raise HTTPException(
            status_code=400,
            detail="Error: host_id = 0",
            headers={"Error": "EndpointParameterError", "Msg": "host_id = 0"},
        )

    if not valid_reservation(rsrv):
        raise HTTPException(
            status_code=400,
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
        existing_reservation: Reservation = db.exec(statement).first()

    if existing_reservation is not None:
        ic("Dubbelbokning")
        ic(existing_reservation)
        return False

    return True


def place_available(reservation: ReservationDB):
    """
    Checks if the current reservation from add_reservation can fit in the
    available places of the host
    """

    host_id = reservation.host_id
    with get_session() as db:
        statement = (
            select(HostDB.total_available_places)
            .where(HostDB.id == host_id)
        )
        # Possibility to retrieve value as int instead of tuple?
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