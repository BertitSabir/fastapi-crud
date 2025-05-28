import pytest
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from src.models.hero import Hero
from src.models.team import Team


@pytest.fixture(name="session")
def session_fixture():
    # Create an in-memory SQLite database
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Heroes
        hero_batman = Hero(name="Batman", secret_name="Bruce Wayne", age=35)
        hero_superman = Hero(name="Superman", secret_name="Clark Kent", age=30)
        hero_flash = Hero(name="Flash", secret_name="Barry Allen", age=28)
        hero_cyborg = Hero(name="Cyborg", secret_name="Victor Stone", age=25)
        # Teams
        team_justice_league = Team(
            name="Justice League",
            headquarters="Gotham",
            heroes=[hero_batman, hero_superman, hero_flash],
        )
        team_humanity = Team(
            name="Humanity",
            headquarters="Earth",
        )
        # Link heroes to teams:
        team_justice_league.heroes = [hero_batman, hero_superman]
        team_humanity.heroes = [hero_cyborg, hero_flash]
        session.add(team_justice_league)
        session.add(team_humanity)
        session.commit()
        session.refresh(team_justice_league)
        session.refresh(team_humanity)

        yield session

        # Clean up the memory database after tests
        SQLModel.metadata.drop_all(engine)
