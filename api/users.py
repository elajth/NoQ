from typing import Optional
from datetime import datetime
from fastapi import Depends, APIRouter
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models.user import User
from db.db_setup import get_db, engine

class UserBase(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    unokod: str
    updated_at: datetime
    created_at: datetime

router = APIRouter()


@router.get("/users")
def get_users(skip: int = 0, limit: int = 100):
    with Session(engine) as session:
        user_list = session.query(User).offset(skip).limit(limit).all()
    return user_list


# @router.post("/users")
# async def create_user(user: UserBase):
#     users.append(user)
#     return "Success"


# @router.get("/users/{id}")
# async def get_user(id: int):
#     return {"user": users[id]}
