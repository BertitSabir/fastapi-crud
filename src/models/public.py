from typing import Optional

from src.models.hero import HeroBase
from src.models.team import TeamBase


class TeamPublic(TeamBase):
    id: int


class HeroPublic(HeroBase):
    id: int


class TeamPublicWithHeroes(TeamPublic):
    heroes: list['HeroPublic'] = []


class HeroPublicWithTeam(HeroPublic):
    team: Optional['TeamPublic'] = None
