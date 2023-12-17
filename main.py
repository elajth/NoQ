from fastapi import FastAPI

from api import hosts, reservations, users, common_services, rooms

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
app.include_router(rooms.router)
app.include_router(common_services.router)
