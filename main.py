from fastapi import FastAPI
from datetime import datetime

from api import hosts, reservations, users
from db.db_setup import engine
from db.models import host, reservation, user

user.Base.metadata.create_all(bind=engine)
# reservation.Base.metadata.create_all(bind=engine)
# host.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NoQ booking app",
    description="App for users to search beds and create reservations",
    version="0.0.1",
    contact={
        "name": "Johan",
        "email": "elajth@proton.me",
    },
)

@app.get("/")
def health_status():
    return {"Health status": "noQ API backend status = OK"}

app.include_router(users.router)
app.include_router(hosts.router)
app.include_router(reservations.router)