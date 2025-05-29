import pytest
from src.models.hero import HeroCreate, HeroUpdate, Hero

from src.crud.hero import (
    get_heroes,
    get_hero_by_id,
    create_hero,
    update_hero,
    delete_hero,
    HeroNotFoundError,
    hash_password,
)


def test_create_hero(session):
    # Arrange
    password = "password"
    hero = HeroCreate(
        name="Spiderman 3",
        secret_name="Miles Morales",
        age=25,
        password=password,
        team_id=1,
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
    # Heroes
    hero_batman = Hero(name="Batman", secret_name="Bruce Wayne", age=35)
    hero_superman = Hero(name="Superman", secret_name="Clark Kent", age=30)
    hero_flash = Hero(name="Flash", secret_name="Barry Allen", age=28)
    hero_cyborg = Hero(name="Cyborg", secret_name="Victor Stone", age=25)
    heroes = [hero_batman, hero_superman, hero_flash, hero_cyborg]
    for hero in heroes:
        create_hero(hero, session)

    # Act
    heroes = get_heroes(session=session, offset=0, limit=100)

    # Assert
    assert len(heroes) == 5
    assert heroes[0].id == 1
    assert heroes[1].id == 2
    assert heroes[2].id == 3
    assert heroes[3].id == 4


def test_get_existing_hero_by_id(session, batman_is_here):
    # Arrange
    hero_id = batman_is_here.id

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


def test_update_hero(session, batman_is_here):
    # Arrange
    new_password = "newpassword"
    hashed_new_password = hash_password(password=new_password)
    hero_batman = batman_is_here
    updated_hero = HeroUpdate(name="Spiderman 3", age=31, password=new_password)

    # Act
    updated_hero = update_hero(
        hero_id=hero_batman.id, hero=updated_hero, session=session
    )

    # Assert
    assert updated_hero.id == hero_batman.id
    assert updated_hero.name == "Spiderman 3"
    assert updated_hero.age == 31
    assert updated_hero.hashed_password == hashed_new_password


def test_delete_hero(session, batman_is_here):
    # Arrange
    hero_id = batman_is_here.id

    # Act
    deleted = delete_hero(hero_id=hero_id, session=session)

    # Assert
    assert deleted

    # Verify the hero is deleted
    with pytest.raises(HeroNotFoundError, match=f"Hero with id {hero_id} not found"):
        get_hero_by_id(hero_id=hero_id, session=session)
