import pytest
from faker import Faker
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel
from starlette.testclient import TestClient

from src.crud.auth_session import create_auth_session
from src.crud.hero import create_hero
from src.crud.team import create_team
from src.crud.user import create_user
from src.dependencies import get_session
from src.main import app
from src.models.auth_session import AuthSessionCreate
from src.models.hero import Hero
from src.models.team import Team, TeamCreate
from src.models.user import UserCreate


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture(name="session", scope="module")
def session_fixture():
    test_db_url = "testing.db"
    # Create an in-memory SQLite database
    engine = create_engine(
        f"sqlite:///{test_db_url}",
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

        # Clean up the memory database after tests
        SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session):
    # Heroes
    hero_batman = Hero(name="Batman", secret_name="Bruce Wayne", age=35)  # noqa: S106
    hero_superman = Hero(name="Superman", secret_name="Clark Kent", age=30)  # noqa: S106
    hero_flash = Hero(name="Flash", secret_name="Barry Allen", age=28)  # noqa: S106
    hero_cyborg = Hero(name="Cyborg", secret_name="Victor Stone", age=25)  # noqa: S106
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

    def override_get_session():
        return session

    app.dependency_overrides[get_session] = override_get_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def batman_is_here(session):
    hero_batman = Hero(name="Batman", secret_name="Bruce Wayne", age=35)  # noqa: S106
    return create_hero(hero_batman, session)


@pytest.fixture
def team_avengers_is_here(session):
    team = TeamCreate(
        name="Avengers",
        headquarters="LA",
    )
    return create_team(team, session)


@pytest.fixture
def test_password():
    return "fixed_test_password_123"


@pytest.fixture(name="user")
def user_fixture(session, fake, test_password):
    user_create = UserCreate(
        username=fake.user_name(),
        full_name=fake.name(),
        email=fake.email(),
        password=test_password,
    )
    user = create_user(user=user_create, session=session)
    return user


@pytest.fixture(name="auth_session")
def auth_session_fixture(session, user):
    auth_session = create_auth_session(
        auth_session=AuthSessionCreate(user_id=user.id),
        session=session,
    )
    return auth_session
