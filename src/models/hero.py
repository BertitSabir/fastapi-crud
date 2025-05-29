from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.models.team import Team  # pragma: no cover


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id", ondelete="CASCADE")


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str = Field(default=None, max_length=50)
    hashed_password: str | None = Field(default=None)

    team: Optional["Team"] = Relationship(back_populates="heroes")


class HeroCreate(HeroBase):
    password: str | None = None


class HeroUpdate(HeroCreate):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
    password: str | None = None
    team_id: int | None = None
