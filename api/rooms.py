from typing import List
from fastapi import APIRouter, HTTPException, Depends
from icecream import ic
from sqlmodel import select, Session
from sqlalchemy import func
from db.db_setup import yield_session, get_session, engine
from db.models.room import (
    RoomDB,
    RoomAdd,
)
# from db.models.host import HostDB
# will be used later

router = APIRouter()


@router.get("/rooms", response_model=List[RoomDB])
async def list_rooms(
    *, session: Session = Depends(yield_session), skip: int = 0, limit: int = 100
):
    rooms = session.exec(select(RoomDB).offset(skip).limit(limit)).all()
    return rooms


@router.post("/rooms", response_model=RoomDB)
async def add_room(*, session: Session = Depends(yield_session), room: RoomAdd):
    db_room: RoomDB = RoomDB.model_validate(room)
    session.add(db_room)
    session.commit()
    session.refresh(db_room)
    return db_room
