from typing import Optional
from sqlmodel import Field, SQLModel


class DBModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
