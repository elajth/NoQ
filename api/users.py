from typing import Optional, List
import fastapi
from datetime import datetime
from pydantic import BaseModel

router = fastapi.APIRouter()

users = []

class User(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    unokod: str
    reservation_uuid: int

@router.get("/users", response_model=List[User])
async def get_users():
    return users


@router.post("/users")
async def create_user(user: User):
    users.append(user)
    return "Success"

@router.get("/users/{id}")
async def get_user(id: int):
    
    return { "user": users[id] }