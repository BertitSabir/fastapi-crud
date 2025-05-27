"""
Specs:
- id and secret_name shouldn't be exposed publicly.
- id must be filled with the database not by the logic.
- we should only expose and allow updating public data: age and name.
- we should distinguish schemas from database model:
Hero -> table model: as a convention we use Hero as SQLModel will infer the table name from it.
HeroBase -> data model: fields shared by all models. name, age
HeroPublic ->   data model: id, name, age
HeroCreate ->   data model: name, age, secret_name
HeroUpdate ->   data_model: name, age, secret_name
"""

from sqlmodel import SQLModel, Field


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str = Field(default=None, max_length=50)
    hashed_password: str | None = Field(default=None)


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    password: str


class HeroUpdate(HeroCreate):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
    password: str | None = None
