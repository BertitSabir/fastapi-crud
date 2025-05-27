import pytest
from sqlmodel import SQLModel, Session, create_engine
from src.models.hero import Hero, HeroCreate

from src.crud.hero import (
    list_heroes,
    get_hero,
    create_hero,
    update_hero,
    delete_hero,
    HeroNotFoundError,
)


@pytest.fixture(name="session")
def session_fixture():
    # Create an in-memory SQLite database
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Initialize the database with some test data
        hero_1 = Hero(name="Spiderman 1", secret_name="Peter Parker", age=30)
        hero_2 = Hero(name="Spiderman 2", secret_name="Ben Reilly", age=28)
        session.add(hero_1)
        session.add(hero_2)
        session.commit()
        session.refresh(hero_1)
        session.refresh(hero_2)

        yield session

        # Clean up the memory database after tests
        SQLModel.metadata.drop_all(engine)


def test_create(session):
    # Arrange
    hero = HeroCreate(
        name="Spiderman 3", secret_name="Miles Morales", age=25, password="password"
    )

    # Act
    created_hero = create_hero(hero=hero, session=session)

    # Assert
    assert created_hero.id is not None
    assert created_hero.name == "Spiderman 3"
    assert created_hero.secret_name == "Miles Morales"
    assert created_hero.age == 25


def test_list(session):
    # Arrange
    # Act
    heroes = list_heroes(session=session, offset=0, limit=100)

    # Assert
    assert len(heroes) == 2
    assert heroes[0].id == 1
    assert heroes[1].id == 2


def test_get_hero_success(session):
    # Arrange
    hero_id = 1

    # Act
    hero = get_hero(hero_id=hero_id, session=session)

    # Assert
    assert hero.id == hero_id
    assert hero.name == "Spiderman 1"
    assert hero.secret_name == "Peter Parker"
    assert hero.age == 30


def test_get_not_found_hero(session):
    # Arrange
    hero_id = 0

    # Act & Assert
    with pytest.raises(HeroNotFoundError, match=f"Hero with id {hero_id} not found"):
        get_hero(hero_id=hero_id, session=session)


def test_update_hero(session):
    # Arrange
    original_hero = get_hero(hero_id=1, session=session)
    updated_hero = Hero(name="Spiderman 3", age=31)

    # Act
    updated_hero = update_hero(
        hero_id=original_hero.id, hero=updated_hero, session=session
    )

    # Assert
    assert updated_hero.id == original_hero.id
    assert updated_hero.name == "Spiderman 3"
    assert updated_hero.age == 31


def test_delete_hero(session):
    # Arrange
    hero_id = 1

    # Act
    result = delete_hero(hero_id=hero_id, session=session)

    # Assert
    assert result == {"ok": True}

    # Verify the hero is deleted
    with pytest.raises(HeroNotFoundError, match=f"Hero with id {hero_id} not found"):
        get_hero(hero_id=hero_id, session=session)
