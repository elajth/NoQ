from fastapi import FastAPI, HTTPException

from sqlmodel import (
    Field,
    SQLModel,
    Session,
    Relationship,
    create_engine,
    select
)


# Database models
class Parent(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    children: list["Child"] = Relationship(back_populates="parent")


class Child(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    parent_id: int = Field(foreign_key="parent.id")
    parent: Parent = Relationship(back_populates="children")


# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

# FastAPI setup
app = FastAPI()


# FastAPI endpoints
@app.post("/parents/", response_model=Parent)
def create_parent(parent: Parent):
    with Session(engine) as session:
        db_parent = Parent.from_orm(parent)
        session.add(db_parent)
        session.commit()
        session.refresh(db_parent)
    return db_parent


@app.post("/children/", response_model=Child)
def create_child(child: Child):
    with Session(engine) as session:
        db_child = Child.from_orm(child)
        session.add(db_child)
        session.commit()
        session.refresh(db_child)
    return db_child


@app.get("/parent_with_children/{parent_id}", response_model=Parent)
def get_parent_with_children(parent_id: int):
    with Session(engine) as session:
        # db_parent = session.get(Parent, parent_id)
        db_parent = session.execute(
            select(Parent)
            .options(selectinload(Parent.children))
            .where(Parent.id == parent_id)
        ).scalar_one_or_none()
        if db_parent is None:
            raise HTTPException(status_code=404, detail="Parent not found")
        return db_parent


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
