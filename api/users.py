from typing import List
from fastapi import Depends, APIRouter, HTTPException
from db.models.user import UserDB, User, UserAdd, UserUpdate
from db.db_setup import yield_session, engine
from sqlmodel import select, Session

router = APIRouter()


@router.get("/users", response_model=List[User])
async def list_users(*, session: Session = Depends(yield_session), skip: int = 0, limit: int = 100):
    users = session.exec(select(UserDB).offset(skip).limit(limit)).all()
    return users


@router.post("/users", response_model=User)
async def add_user(*, session: Session = Depends(yield_session), user: UserAdd):
    db_user: UserDB = UserDB.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users/{id}")
async def get_user(*, session: Session = Depends(yield_session)):
    user = session.get(UserDB, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{id}", response_model=User)
def update_user(*, session: Session = Depends(yield_session), user: UserUpdate):
    db_user = session.get(UserDB, id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
