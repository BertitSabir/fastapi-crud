from sqlmodel import Session, select
from typing import Sequence

from src.models.hero import HeroBase, Hero, HeroCreate, HeroPublic, HeroUpdate


class HeroNotFoundError(Exception):
    def __init__(self, message: str = "Hero not found"):
        super().__init__(message)
        self.message = message


def hash_password(password: str) -> str:
    return f"hashed_{password}"


def create_hero(hero: HeroCreate, session: Session) -> HeroBase:
    hashed_password = hash_password(password=hero.password)
    extra_data = {"hashed_password": hashed_password}
    db_hero = Hero.model_validate(hero, update=extra_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


def list_heroes(
    session: Session,
    offset: int = 0,
    limit: int = 100,
) -> Sequence[HeroPublic]:
    statement = select(Hero).offset(offset).limit(limit)
    heroes = session.exec(statement=statement).all()
    return heroes


def get_hero(hero_id: int, session: Session) -> HeroPublic:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HeroNotFoundError(message=f"Hero with id {hero_id} not found")
    return hero


def update_hero(hero_id: int, hero: HeroUpdate, session: Session) -> HeroBase:
    hero_db = get_hero(hero_id, session)
    # get only the hero data that was set in the request
    hero_data = hero.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in hero_data:
        hashed_password = hash_password(hero_data["password"])
        extra_data["hashed_password"] = hashed_password
    # update the hero_db with the new data
    hero_db.sqlmodel_update(hero_data, update=extra_data)
    session.add(hero_db)
    session.commit()
    # refresh the hero_db to get the db state
    session.refresh(hero_db)
    return hero_db


def delete_hero(hero_id: int, session: Session) -> dict:
    hero_db = get_hero(hero_id, session)
    session.delete(hero_db)
    session.commit()
    return {"ok": True}
