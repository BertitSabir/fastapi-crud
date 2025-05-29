from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.models.hero import Hero  # pragma: no cover


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str | None = Field(default=None)


class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    heroes: list["Hero"] = Relationship(back_populates="team", passive_deletes="all")


class TeamCreate(TeamBase):
    pass


class TeamUpdate(TeamBase):
    name: str | None = None
    headquarters: str | None = None
