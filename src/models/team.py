from sqlmodel import SQLModel, Field, Relationship


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    heroes: list['Hero'] = Relationship(back_populates='team')


class TeamCreate(TeamBase):
    pass


class TeamUpdate(TeamBase):
    name: str | None = None
    headquarters: str | None = None


class TeamPublic(TeamBase):
    id: int