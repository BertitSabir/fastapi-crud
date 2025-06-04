from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from starlette import status

from src.crud.team import (
    TeamNotFoundError,
    create_team,
    delete_team,
    get_team_by_id,
    get_teams,
)
from src.crud.team import (
    update_team as update_repo,
)
from src.dependencies import SessionDep
from src.models.public import TeamPublic, TeamPublicWithHeroes
from src.models.team import Team, TeamCreate, TeamUpdate

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=TeamPublic)
async def create(team: TeamCreate, session: SessionDep) -> Team:
    return create_team(team=team, session=session)


@router.get(path="/", response_model=list[TeamPublicWithHeroes])
async def list_teams(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Team]:
    return get_teams(session=session, offset=offset, limit=limit)


@router.get(path="/{team_id}", response_model=TeamPublicWithHeroes)
async def get_team(
    team_id: int,
    session: SessionDep,
) -> Team:
    try:
        return get_team_by_id(team_id=team_id, session=session)
    except TeamNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.patch(path="/{team_id}", response_model=TeamPublic)
async def update(team_id: int, team: TeamUpdate, session: SessionDep) -> Team:
    try:
        return update_repo(team_id=team_id, team=team, session=session)
    except TeamNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(team_id: int, session: SessionDep):
    try:
        delete_team(team_id=team_id, session=session)
    except TeamNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
