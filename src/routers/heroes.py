from typing import Annotated

from fastapi import Query, HTTPException, APIRouter
from starlette import status

from src.crud.hero import create_hero, get_heroes, get_hero_by_id, HeroNotFoundError, update_hero as update_repo, \
    delete_hero as delete_repo
from src.dependencies import SessionDep
from src.models.hero import HeroPublic, HeroCreate, HeroUpdate

router = APIRouter(
    prefix='/heroes',
    tags=['Heroes']
)
@router.post(
    path="/", status_code=status.HTTP_201_CREATED, response_model=HeroPublic
)
async def create_heros(hero: HeroCreate, session: SessionDep):
    return create_hero(hero=hero, session=session)


@router.get(path="/", response_model=list[HeroPublic])
async def read_heroes(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return get_heroes(session=session, offset=offset, limit=limit)


@router.get(path="/{hero_id}", response_model=HeroPublic)
async def read_hero(
    hero_id: int,
    session: SessionDep,
):
    try:
        return get_hero_by_id(hero_id=hero_id, session=session)
    except HeroNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.patch(path="/{hero_id}", response_model=HeroPublic)
async def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    try:
        return update_repo(hero_id=hero_id, hero=hero, session=session)
    except HeroNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.delete("/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hero(hero_id: int, session: SessionDep):
    try:
        delete_repo(hero_id=hero_id, session=session)
    except HeroNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
