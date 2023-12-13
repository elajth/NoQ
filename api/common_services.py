from fastapi import APIRouter

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
    return {
        "Health status": "NoQ API backend status = OK. " + count_records_in_database()
    }


@router.get("/generate")
async def do_generate():
    try:
        create_db_tables(True)

        hosts = add_hosts()

        reservations = add_reservation()

        users = add_users()

        return {"hosts": hosts, "users": users, "reservations": reservations}

    except Exception:
        return "Testdata finns redan."
