from fastapi import FastAPI
from datetime import datetime

from api import hosts, reservations, users
from db.db_setup import engine
from db.models import hosts, reservations, users

#users.Base.metadata.create_all(bind=engine)
reservations.Base.metadata.create_all(bind=engine)
hosts.Base.metadata.create_all(bind=engine)

from api import users, reservations, hosts

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
#app.include_router(hosts.router)
app.include_router(reservations.router)