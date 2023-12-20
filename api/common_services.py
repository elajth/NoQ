import os
from icecream import ic
from fastapi import APIRouter
from fastapi.responses import HTMLResponse


from generate import (
    create_db_tables,
    add_hosts,
    add_reservation,
    add_users,
    count_records_in_database,
)

router = APIRouter()


@router.get("/")
def health_status():
    path = os.getcwd()
    filename = path + "/templates/index.html"
    data = ""
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as file:
            data = file.read()
    engine = create_db_tables(False)
    status = "API status = OK <br/><br/>Data:" + count_records_in_database(engine)
    html = data.replace("{health_status}", status)
    return HTMLResponse(content=html)


@router.get("/generate")
async def do_generate():
    try:
        engine = create_db_tables(True)

        hosts = add_hosts(engine)

        users = add_users(engine)

        reservations = add_reservation(engine)

        return {"hosts": hosts, "users": users, "reservations": reservations}

    except Exception as ex:
        return ex
