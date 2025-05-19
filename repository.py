from sqlmodel import Session, select
from typing import Sequence

from models import HeroBase, Hero


class HeroNotFoundError(Exception):
    def __init__(self, message: str = "Hero not found"):
        super().__init__(message)
        self.message = message


def create_hero(hero: HeroBase, session: Session) -> HeroBase:
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


def list_heroes(
    session: Session,
    offset: int = 0,
    limit: int = 100,
) -> Sequence[Hero]:
    statement = select(Hero).offset(offset).limit(limit)
    heroes = session.exec(statement=statement).all()
    return heroes


def get_hero(hero_id: int, session:Session) -> HeroBase:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HeroNotFoundError(message=f"Hero with id {hero_id} not found")
    return hero


def update_hero(
    hero_id: int,
    hero: HeroBase,
    session: Session
) -> HeroBase:
    hero_db = get_hero(hero_id, session)
    # get only the hero data that was set in the request
    hero_data = hero.model_dump(exclude_unset=True)
    # update the hero_db with the new data
    hero_db.sqlmodel_update(hero_data)
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

