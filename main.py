from fastapi import FastAPI, Query, HTTPException, status
from typing import Annotated
from sqlmodel import select

from db import lifespan
from dependencies import SessionDep
from models import Hero, HeroPublic, HeroCreate, HeroUpdate

# Create FastAPI app:
app = FastAPI(lifespan=lifespan)  # noqa


@app.post(
    path="/heroes/",
    status_code=status.HTTP_201_CREATED,
    response_model=HeroPublic
)
async def create_heros(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get(
    path="/heroes/",
    response_model=list[HeroPublic]
)
async def read_heroes(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    statement = select(Hero).offset(offset).limit(limit)
    heroes = session.exec(statement=statement).all()
    return heroes


@app.get(
    path="/heroes/{hero_id}",
    response_model=HeroPublic
)
async def read_hero(
    hero_id: int,
    session: SessionDep,
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )
    return hero


@app.patch(
    path="/heroes/{hero_id}",
    response_model=HeroPublic
)
async def update_hero(
    hero_id: int,
    hero: HeroUpdate,
    session: SessionDep
):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not Found"
        )
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db


@app.delete("/heroes/{hero_id}")
async def delete_hero(hero_id: int, session: SessionDep) -> dict:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not Found"
        )
    session.delete(hero)
    session.commit()
    return {"ok": True}
