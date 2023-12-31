# Copied from
# https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/
#

from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, func
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import (
    Field,
    Relationship,
    DateTime,
    Session,
    SQLModel,
    create_engine,
    select,
)


class DBCommon(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class TeamBase(SQLModel):
    """
    Primary fields
    """

    name: str = Field(index=True, description="Public name for Team")
    headquarters: str = Field(index=True, description="Track name for headquarters")


# TeamDB is named Team in SQLModel example,
# but since it is never used I've renamed it
class TeamDB(TeamBase, DBCommon, table=True):
    """
    DB Access
    """

    __tablename__ = "team"

    heroes: List["Hero"] = Relationship(back_populates="team")


class TeamAdd(TeamBase):
    """
    Add team
    """

    pass


# Team is named TeamRead in SQLModel example,
# but since Team is more descriptive and available I've renamed it
class Team(TeamBase):
    """
    Team who owns and trains heros
    """

    id: int


class TeamUpdate(SQLModel):
    """
    Team with optional fields
    """

    id: Optional[int] = None
    name: Optional[str] = None
    headquarters: Optional[str] = None


class HeroBase(SQLModel):
    """
    Primary fields
    """

    name: str = Field(index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, DBCommon, table=True):
    """
    DB Access
    """

    __tablename__ = "hero"

    team: Optional[TeamDB] = Relationship(back_populates="heroes")


# Hero is named HeroRead in SQLModel example,
# but since Team is more descriptive and available I've renamed it
class HeroRead(HeroBase):
    """
    Hero is a horse in training by a Team
    """

    id: int


class HeroCreate(HeroBase):
    """
    Add record
    """

    pass


class HeroUpdate(SQLModel):
    """
    Hero with optional fields
    """

    name: Optional[str] = None
    team_id: Optional[int] = None


# Note: Without any back_populate makes it
# possible to retrieve a deep json-structure
class HeroReadWithTeam(HeroRead):
    """
    Hero with its Team details
    """

    team: Optional[Team] = None


# Note: Without any back_populate makes it
# possible to retrieve a deep json-structure
class TeamWithHeroes(Team):
    """
    Team with a list of Heroes
    """

    heroes: List[HeroRead] = []


sqlite_file_name = "heroes.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    team_solvalla = TeamDB(name="Stig H Johansson", headquarters="Solvalla")
    team_axevalla = TeamDB(name="André Eklundh", headquarters="Axevalla")
    hero_cannon = Hero(name="CANNON BALL")
    hero_dakota = Hero(name="DAKOTA")
    hero_forth_vox = Hero(name="FOURTH VOX")

    with Session(engine) as session:
        # Add Team
        session.add(team_solvalla)
        session.add(team_axevalla)
        session.commit()
        # session.refresh(team_solvalla)
        # Add Hero
        hero_cannon.team = team_solvalla
        hero_dakota.team = team_solvalla
        hero_forth_vox.team = team_axevalla
        session.commit()


def yield_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/", response_model=HeroRead)
def add_hero(*, session: Session = Depends(yield_session), hero: HeroCreate):
    db_hero = Hero.model_validate(
        hero
    )  # TODO: Byt till Hero.model_validate(team) vid ny version av SQLModel
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=List[HeroRead])
def list_heroes(
    *,
    session: Session = Depends(yield_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroReadWithTeam)
def read_hero(*, session: Session = Depends(yield_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(
    *, session: Session = Depends(yield_session), hero_id: int, hero: HeroUpdate
):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero.model_dump(exclude_unset=True)

    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.delete("/heroes/{hero_id}")
def delete_hero(*, session: Session = Depends(yield_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}


@app.post("/teams/", response_model=Team)
def add_team(*, session: Session = Depends(yield_session), team: TeamAdd):
    db_team = TeamDB.model_validate(
        team
    )  
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.get("/teams/", response_model=List[Team])
def list_teams(
    *,
    session: Session = Depends(yield_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    teams = session.exec(select(TeamDB).offset(offset).limit(limit)).all()
    return teams


@app.get("/teams/{team_id}", response_model=TeamWithHeroes)
def read_team(*, team_id: int, session: Session = Depends(yield_session)):
    team = session.get(TeamDB, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.patch("/teams/{team_id}", response_model=Team)
def update_team(
    *,
    session: Session = Depends(yield_session),
    team_id: int,
    team: TeamUpdate,
):
    db_team = session.get(TeamDB, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.model_dump(
        exclude_unset=True
    )  # TODO: Byt till team.model_dump(exclude_unset=True) vid ny version av SQLModel
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.delete("/teams/{team_id}")
def delete_team(*, session: Session = Depends(yield_session), team_id: int):
    team = session.get(TeamDB, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}
