from typing import Optional, List
from datetime import datetime
from fastapi import Depends, APIRouter
from pydantic import BaseModel
from db.models.user import User
from db.db_setup import get_db, engine
from sqlmodel import select, Session

router = APIRouter()

@router.get("/user", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 100):
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users

#@router.get("/user")
#def get_users(skip: int = 0, limit: int = 100):
#    with Session(engine) as session:
#        user_list = session.query(User).offset(skip).limit(limit).all()
#    return user_list


# @router.post("/users")
# async def create_user(user: UserBase):
#     users.append(user)
#     return "Success"


# @router.get("/users/{id}")
# async def get_user(id: int):
#     return {"user": users[id]}