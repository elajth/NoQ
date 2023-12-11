from typing import List
from fastapi import APIRouter, HTTPException, Depends
from icecream import ic
from sqlmodel import select, Session
from db.db_setup import yield_session, get_session, engine
from db.models.reservation import (
    ReservationDB,
    Reservation,
    Reservation_User,
    ReservationAdd,
)

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


@router.post("/reservations", response_model=Reservation)
async def add_reservation(
    *, session: Session = Depends(yield_session), reservation: ReservationAdd
):
    rsrv: ReservationDB = ReservationDB.model_validate(reservation)

    if reservation.user_id < 1:
        ic(reservation)
        raise HTTPException(
            status_code=400,  # https://docs.oracle.com/en/cloud/saas/marketing/eloqua-develop/Developers/GettingStarted/APIRequests/Validation-errors.htm
            detail="Error: user_id = 0",
            headers={"Error": "EndpointParameterError", "Msg": "user_id = 0"},
        )

    if reservation.host_id < 1:
        ic(reservation)
        raise HTTPException(
            status_code=400,  # https://docs.oracle.com/en/cloud/saas/marketing/eloqua-develop/Developers/GettingStarted/APIRequests/Validation-errors.htm
            detail="Error: host_id = 0",
            headers={"Error": "EndpointParameterError", "Msg": "host_id = 0"},
        )

    if not valid_reservation(rsrv):
        raise HTTPException(
            status_code=400,  # https://docs.oracle.com/en/cloud/saas/marketing/eloqua-develop/Developers/GettingStarted/APIRequests/Validation-errors.htm
            detail="Dubbelbokning samma dag för denna brukare",
            headers={"Error": "UniquenessRequirement", "Msg": "User is booked already"},
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
