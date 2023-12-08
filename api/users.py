from typing import Optional, List
from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from db.models.user import User, UserRead, UserCreate, UserPatch
from db.db_setup import get_db, engine
from sqlmodel import select, Session

router = APIRouter()


@router.get("/users", response_model=List[User])
async def list_users(skip: int = 0, limit: int = 100):
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users


@router.post("/users", response_model=UserRead)
async def create_new_user(user: UserCreate):
    with Session(engine) as session:
        db_user: User = User.from_orm(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user


@router.get("/users/{id}")
async def get_user(id: int):
    with Session(engine) as session:
        user = session.get(User, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


@router.patch("/users/{id}", response_model=UserRead)
def update_user(id: int, user: UserPatch):
    with Session(engine) as session:
        db_user = session.get(User, id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
