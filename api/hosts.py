from typing import List
from icecream import ic
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from db.db_setup import yield_session
from db.models.host import HostDB, Host, Host_Reservations, HostAdd, HostUpdate
from db.models.reservation import ReservationDB, Reservation_User

router = APIRouter()


@router.get("/hosts", response_model=List[Host])
async def list_hosts(
    *, session: Session = Depends(yield_session), skip: int = 0, limit: int = 100
):
    hosts = session.exec(select(HostDB).offset(skip).limit(limit)).all()
    return hosts


@router.post("/hosts", response_model=Host)
async def add_host(*, session: Session = Depends(yield_session), host: HostAdd):
    db_host: HostDB = HostDB.model_validate(host)
    session.add(db_host)
    session.commit()
    session.refresh(db_host)
    return db_host


@router.get("/hosts/{id}", response_model=Host_Reservations)
async def get_host(*, id: int, session: Session = Depends(yield_session)):
    host = session.get(HostDB, id)

    if not host:
        raise HTTPException(status_code=404, detail="Host not found")
    return host


@router.patch("/hosts/{id}", response_model=Host)
def update_host(*, session: Session = Depends(yield_session), host: HostUpdate):
    db_host = session.get(HostDB, id)
    if not db_host:
        raise HTTPException(status_code=404, detail="Host not found")
    host_data = host.model_dump(exclude_unset=True)
    for key, value in host_data.items():
        setattr(db_host, key, value)
    session.add(db_host)
    session.commit()
    session.refresh(db_host)
    return db_host


@router.get("/hosts/{host_id}/reservations", response_model=List[Reservation_User])
async def list_reservations_for_host(
    *, host_id: int, session: Session = Depends(yield_session)
):
    stmt = select(ReservationDB).where(ReservationDB.host_id == host_id)

    reservations = session.exec(stmt).all()

    if not reservations:
        raise HTTPException(status_code=404, detail="No reservations found")
    ic(reservations)

    return reservations
