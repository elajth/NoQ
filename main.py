from typing import Optional, List
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from datetime import datetime

from api import hosts, reservations, users

app = FastAPI(
    title="NoQ booking app",
    description="App for users to search beds and create reservations",
    version="0.0.1",
    contact={
        "name": "Johan",
        "email": "elajth@proton.me",
    },
)
app.include_router(users.router)
app.include_router(hosts.router)
app.include_router(reservations.router)