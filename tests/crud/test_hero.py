import pytest
from src.models.hero import Hero, HeroCreate, HeroUpdate

from src.crud.hero import (
    get_heroes,
    get_hero_by_id,
    create_hero,
    update_hero,
    delete_hero,
    HeroNotFoundError, hash_password,
)


def test_create_hero(session):
    # Arrange
    password = 'password'
    hero = HeroCreate(
        name="Spiderman 3", secret_name="Miles Morales", age=25, password=password, team_id=1
    )

    # Act
    created_hero = create_hero(hero=hero, session=session)

    # Assert
    assert created_hero.id is not None
    assert created_hero.name == "Spiderman 3"
    assert created_hero.secret_name == "Miles Morales"
    assert created_hero.age == 25
    assert created_hero.hashed_password == hash_password(password=password)


def test_list(session):
    # Arrange
    # Act
    heroes = get_heroes(session=session, offset=0, limit=100)

    # Assert
    assert len(heroes) == 4
    assert heroes[0].id == 1
    assert heroes[1].id == 2
    assert heroes[2].id == 3
    assert heroes[3].id == 4


def test_get_existing_hero_by_id(session):
    # Arrange
    hero_id = 1

    # Act
    hero = get_hero_by_id(hero_id=hero_id, session=session)

    # Assert
    assert hero.id == hero_id
    assert hero.name == "Batman"
    assert hero.secret_name == "Bruce Wayne"
    assert hero.age == 35


def test_get_unexisting_hero_by_id(session):
    # Arrange
    hero_id = 0

    # Act & Assert
    with pytest.raises(HeroNotFoundError, match=f"Hero with id {hero_id} not found"):
        get_hero_by_id(hero_id=hero_id, session=session)


def test_update_hero(session):
    # Arrange
    new_password = 'newpassword'
    hashed_new_password = hash_password(password=new_password)
    original_hero = get_hero_by_id(hero_id=1, session=session)
    updated_hero = HeroUpdate(name="Spiderman 3", age=31, password=new_password)

    # Act
    updated_hero = update_hero(
        hero_id=original_hero.id, hero=updated_hero, session=session
    )

    # Assert
    assert updated_hero.id == original_hero.id
    assert updated_hero.name == "Spiderman 3"
    assert updated_hero.age == 31
    assert updated_hero.hashed_password == hashed_new_password


def test_delete_hero(session):
    # Arrange
    hero_id = 1

    # Act
    deleted = delete_hero(hero_id=hero_id, session=session)

    # Assert
    assert deleted

    # Verify the hero is deleted
    with pytest.raises(HeroNotFoundError, match=f"Hero with id {hero_id} not found"):
        get_hero_by_id(hero_id=hero_id, session=session)
