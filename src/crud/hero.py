from sqlmodel import Session, select
from src.models.hero import Hero, HeroCreate, HeroUpdate


class HeroNotFoundError(Exception):
    """
    Custom exception raised when a hero is not found in the database.
    """

    def __init__(self, message: str = "Hero not found"):
        super().__init__(message)
        self.message = message


def hash_password(password: str) -> str:
    """
    Hashes a given password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return f"hashed_{password}"


def create_hero(hero: HeroCreate, session: Session) -> Hero:
    """
    Creates a new hero in the database.

    Args:
        hero (HeroCreate): The hero data to create.
        session (Session): The database session.

    Returns:
        Hero: The created hero object.
    """
    extra_data = {}
    hero_data = hero.model_dump(exclude_unset=True)
    if "password" in hero_data:
        hashed_password = hash_password(password=hero.password)
        extra_data = {"hashed_password": hashed_password}
    db_hero = Hero.model_validate(hero, update=extra_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


def get_heroes(session: Session, offset: int = 0, limit: int = 100) -> list[Hero]:
    """
    Retrieves a list of heroes from the database with pagination.

    Args:
        session (Session): The database session.
        offset (int, optional): The starting index for pagination. Defaults to 0.
        limit (int, optional): The maximum number of heroes to retrieve. Defaults to 100.

    Returns:
        list[Hero]: A list of hero objects.
    """
    statement = select(Hero).offset(offset).limit(limit)
    heroes = session.exec(statement=statement).all()
    return heroes


def get_hero_by_id(hero_id: int, session: Session) -> Hero:
    """
    Retrieves a hero by its ID.

    Args:
        hero_id (int): The ID of the hero to retrieve.
        session (Session): The database session.

    Raises:
        HeroNotFoundError: If the hero with the given ID is not found.

    Returns:
        Hero: The hero object.
    """
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HeroNotFoundError(message=f"Hero with id {hero_id} not found")
    return hero


def update_hero(hero_id: int, hero: HeroUpdate, session: Session) -> Hero:
    """
    Updates an existing hero in the database.

    Args:
        hero_id (int): The ID of the hero to update.
        hero (HeroUpdate): The updated hero data.
        session (Session): The database session.

    Returns:
        Hero: The updated hero object.
    """
    hero_db = get_hero_by_id(hero_id, session)
    hero_data = hero.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in hero_data:
        hashed_password = hash_password(hero_data["password"])
        extra_data["hashed_password"] = hashed_password
    hero_db.sqlmodel_update(hero_data, update=extra_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db


def delete_hero(hero_id: int, session: Session) -> dict:
    """
    Deletes a hero from the database.

    Args:
        hero_id (int): The ID of the hero to delete.
        session (Session): The database session.

    Returns:
        dict: A confirmation of the deletion.
    """
    hero_db = get_hero_by_id(hero_id, session)
    session.delete(hero_db)
    session.commit()
    return True
