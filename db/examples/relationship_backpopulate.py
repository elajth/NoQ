from typing import List, Optional
from datetime import datetime
import time
from icecream import ic
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from sqlalchemy import DateTime, func, Column
from print_code import print_code


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    horses: list["Horse"] = Relationship(back_populates="team")


class Horse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    owner: str
    age: Optional[int] = Field(default=None, index=True)

    type_id: int = Field(default=None, foreign_key="horse_type.id")
    type: "HorseType" = Relationship(back_populates="creatures")

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="horses")

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), onupdate=func.now(), default=None
        )  # sa betyder SQLAlchemy
    )


class HorseType(SQLModel, table=True):
    __tablename__ = "horse_type"
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    creatures: list[Horse] = Relationship(back_populates="type")


print_code(__file__, 10, 43)
sqlite_file_name = "db/examples/horse.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def create_horses():
    warm = HorseType(type="Varm-blooded")
    pony = HorseType(type="Pony")
    gaited = HorseType(type="Gaited")
    with Session(engine) as session:
        session.add(warm)
        session.add(pony)
        session.add(gaited)
        session.commit()
        session.refresh(warm)
        session.refresh(pony)
        session.refresh(gaited)

    # Add Horses

    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="New York")
        team_z_force = Team(name="Z-Force", headquarters="Stockholm")
        team_solvalla = Team(name="Team Solvalla", headquarters="Stockholm")

        hero_deadpond = Horse(
            name="Deadpond", owner="Dive Wilson", team=team_z_force, type=gaited
        )
        hero_rusty_man = Horse(
            name="Rusty-Man",
            owner="Tommy Sharp",
            age=48,
            team=team_preventers,
            type=pony,
        )
        hero_spider_boy = Horse(
            name="Spider-Boy", owner="Pedro Parqueador", type=gaited
        )
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        hero_spider_boy.team = team_solvalla
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        ic("Updated hero:")
        ic(hero_spider_boy)

        hero_black_lion = Horse(
            name="Black Lion", owner="Trevor Challa", age=35, type=pony
        )
        hero_sure_e = Horse(name="Princess Sure-E", owner="Sure-E", type=gaited)
        team_wakaland = Team(
            name="Wakaland",
            headquarters="Wakaland Capital City",
            horses=[hero_black_lion, hero_sure_e],
        )
        session.add(team_wakaland)
        session.commit()
        session.refresh(team_wakaland)
        print("Team Wakaland:", team_wakaland)

        hero_tarantula = Horse(
            name="Tarantula", owner="Natalia Roman-on", age=32, type=gaited
        )
        hero_dr_weird = Horse(name="Dr. Weird", owner="Steve Weird", age=36, type=warm)
        hero_cap = Horse(
            name="Captain North America",
            owner="Esteban Rogelios",
            age=9,
            type=gaited,
        )

        team_preventers.horses.append(hero_tarantula)
        team_preventers.horses.append(hero_dr_weird)
        team_solvalla.horses.append(hero_cap)
        session.add(team_preventers)
        session.add(team_solvalla)
        session.commit()
        session.refresh(hero_tarantula)
        session.refresh(hero_dr_weird)
        session.refresh(hero_cap)
        print("Preventers nbr of horses:", len(team_preventers.horses))


def select_horses():
    print_code(__file__, 147, 11)
    with Session(engine) as session:
        # Alt 1
        statement = select(Horse).where(Horse.name == "Spider-Boy")
        result = session.exec(statement)
        hero_spider_boy = result.one()
        print("Spider-Boy's team alt 1:", hero_spider_boy.team)

        # Alt 2
        statement = select(Team).where(Team.id == hero_spider_boy.team_id)
        result = session.exec(statement)
        team = result.first()
        print("Spider-Boy's team alt 2:", team)


def select_joined_tables():
    with Session(engine) as session:
        print_code(__file__, 163, 4)
        # Alt 1 - Full JOIN btw all objects without filter
        statement = (
            select(Team, HorseType, Horse)
            .join(HorseType)
            .join(Team)
            .order_by(Team.headquarters)
        )
        result = session.exec(statement)
        ic(result.all())

        print_code(__file__, 169, 18)
        # Alt 2 - Full JOIN and WHERE statement for the first object
        statement = (
            select(Horse, HorseType, Team)
            .join(HorseType)
            .join(Team)
            .where(Horse.name == "Spider-Boy")
        )
        result = session.exec(statement)
        hero_spider_boy = result.one()[0]
        hero_spider_boy.owner = "Esteban Rogelios"
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        ic(
            hero_spider_boy.created_at,
            hero_spider_boy.updated_at,
            hero_spider_boy.updated_at - hero_spider_boy.created_at,
        )
        print_code(__file__, 188, 9)
        # Alt 3 - Full JOIN and filter on another object with WHERE
        statement = (
            select(Horse, HorseType, Team)
            .join(HorseType)
            .join(Team)
            .where(HorseType.type == "Pony")
        )
        ponies = session.exec(statement).all()
        ic(ponies)
        print_code(__file__, 198, 4)
        # Alt 4 - List all dependent objects in "creatures" which is a list[]
        statement = select(HorseType).join(Horse).where(HorseType.type == "Gaited")
        type = session.exec(statement).first()
        ic(type.creatures)


def main():
    create_db_and_tables()
    create_horses()
    select_horses()
    select_joined_tables()


if __name__ == "__main__":
    main()
