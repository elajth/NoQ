from sqlmodel import SQLModel, Field, Relationship, create_engine, select, Session, join
from typing import Optional, List
from icecream import ic

engine = create_engine("sqlite://")


class UserInSchema(SQLModel):
    username: str
    phone: str


class User(UserInSchema, table=True):
    __tablename__ = "user_data"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    cars: List["Car"] = Relationship(back_populates="user")


class CarInSchema(SQLModel):
    brand: str
    color: str


class Car(CarInSchema, table=True):
    __tablename__ = "car_data"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user_data.id")
    user: Optional[User] = Relationship(back_populates="cars")

    def __repr__(self) -> str:
        return f"{self.brand} med {self.color.lower()} färg."


stmt = select(Car, User).select_from(join(Car, User))
ic("--------------------------")

with Session(engine) as session:
    SQLModel.metadata.create_all(session.bind)

    user = User(username="Adam", phone="070-124400")
    car = Car(brand="Volvo", color="Grön")
    car.user = user
    session.add(user)
    session.add(car)
    session.commit()

    data = session.exec(stmt).all()
    car = data[0][0]
    ic(type(data[0]))
    print("car:", car)

ic(data[0][0])
ic(car.brand)
# data=[(Car(name='car', user_id=1, id=1, color='color'), User(phone='phone', name='user', id=1))]
