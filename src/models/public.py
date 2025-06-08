from typing import ClassVar, Optional

from src.models.hero import HeroBase
from src.models.team import TeamBase
from src.models.user import UserBase


class TeamPublic(TeamBase):
    id: int


class HeroPublic(HeroBase):
    id: int


class UserPublic(UserBase):
    id: int


class TeamPublicWithHeroes(TeamPublic):
    heroes: ClassVar[list["HeroPublic"]] = []


class HeroPublicWithTeam(HeroPublic):
    team: Optional["TeamPublic"] = None
