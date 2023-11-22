from typing import Optional, List
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI(
    title="NoQ booking app",
    description="App for booking, creating locations and creating users",
    version="0.0.1",
    contact={
        "name": "Johan",
        "email": "elajth@proton.me",
    },
)

locations = []

class Location(BaseModel):
    location_id: int
    location_name: str
    single_beds_max: int
    single_beds_vacant: int
    shared_beds_max: int
    shared_beds_vacant: int
    active: bool
    info: Optional[str] 

@app.get("/locations", response_model=List[Location])
async def get_locations():
    return locations


@app.post("/locations")
async def create_location(location: Location):
    locations.append(location)
    return "Success"

@app.get("/locations/{id}")
async def get_location(
    id: int = Path(..., description="The ID of the location you want to retrieve", ge= 0),
    q: str = Query(None, max_lenght=5)
):
    
    return { "location": locations[id], "Query": q }