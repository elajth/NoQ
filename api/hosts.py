from typing import Optional, List
import fastapi
from datetime import datetime
from pydantic import BaseModel

router = fastapi.APIRouter()

hosts = []

class Host(BaseModel):
    id: int
    name: str
    address1: str
    address2: str
    countOfAvailablePlaces: int
    totalAvailablePlaces: int

@router.get("/hosts", response_model=List[Host])
async def get_hosts():
    return hosts


@router.post("/hosts")
async def create_host(host: Host):
    hosts.append(host)
    return "Success"

@router.get("/hosts/{id}")
async def get_host(id: int):
    
    return { "host": hosts[id] }