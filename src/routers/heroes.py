from typing import Annotated

from fastapi import Query, HTTPException, APIRouter
from starlette import status

from src.crud.hero import (
    create_hero,
    get_heroes,
    get_hero_by_id,
    HeroNotFoundError,
    update_hero,
    delete_hero,
)
from src.dependencies import SessionDep
from src.models.hero import HeroCreate, HeroUpdate, Hero
from src.models.public import HeroPublicWithTeam, HeroPublic

router = APIRouter(prefix="/heroes", tags=["Heroes"])


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=HeroPublic)
async def create(hero: HeroCreate, session: SessionDep) -> Hero:
    return create_hero(hero=hero, session=session)


@router.get(path="/", response_model=list[HeroPublicWithTeam])
async def list_heroes(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    return get_heroes(session=session, offset=offset, limit=limit)


@router.get(path="/{hero_id}", response_model=HeroPublicWithTeam)
async def get_hero(
    hero_id: int,
    session: SessionDep,
) -> Hero:
    try:
        return get_hero_by_id(hero_id=hero_id, session=session)
    except HeroNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.patch(path="/{hero_id}", response_model=HeroPublic)
async def update(hero_id: int, hero: HeroUpdate, session: SessionDep) -> Hero:
    try:
        return update_hero(hero_id=hero_id, hero=hero, session=session)
    except HeroNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.delete("/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(hero_id: int, session: SessionDep):
    try:
        delete_hero(hero_id=hero_id, session=session)
    except HeroNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
