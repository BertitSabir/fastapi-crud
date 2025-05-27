from fastapi import FastAPI, Query, HTTPException, status
from typing import Annotated
from crud.hero import (
    create_hero,
    list_heroes,
    get_hero,
    update_hero as update_repo,
    delete_hero as delete_repo,
    HeroNotFoundError,
)

from database import lifespan
from dependencies import SessionDep
from models.hero import HeroPublic, HeroCreate, HeroUpdate

# Create FastAPI app:
app = FastAPI(lifespan=lifespan)  # noqa


@app.post(
    path="/heroes/", status_code=status.HTTP_201_CREATED, response_model=HeroPublic
)
async def create_heros(hero: HeroCreate, session: SessionDep):
    return create_hero(hero=hero, session=session)


@app.get(path="/heroes/", response_model=list[HeroPublic])
async def read_heroes(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return list_heroes(session=session, offset=offset, limit=limit)


@app.get(path="/heroes/{hero_id}", response_model=HeroPublic)
async def read_hero(
    hero_id: int,
    session: SessionDep,
):
    try:
        return get_hero(hero_id=hero_id, session=session)
    except HeroNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@app.patch(path="/heroes/{hero_id}", response_model=HeroPublic)
async def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    try:
        return update_repo(hero_id=hero_id, hero=hero, session=session)
    except HeroNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@app.delete("/heroes/{hero_id}")
async def delete_hero(hero_id: int, session: SessionDep) -> dict:
    try:
        return delete_repo(hero_id=hero_id, session=session)
    except HeroNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
