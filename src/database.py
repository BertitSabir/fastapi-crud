import os
from contextlib import asynccontextmanager, contextmanager
from typing import Generator

from fastapi import FastAPI
from sqlalchemy import Engine, create_engine
from sqlmodel import Session, SQLModel

from src.models.hero import Hero
from src.models.team import Team


def init_db(session: Session):
    # Heroes
    hero_batman = Hero(name="Batman", secret_name="Bruce Wayne", age=35)
    hero_superman = Hero(name="Superman", secret_name="Clark Kent", age=30)
    hero_flash = Hero(name="Flash", secret_name="Barry Allen", age=28)
    hero_cyborg = Hero(name="Cyborg", secret_name="Victor Stone", age=25)
    # Teams
    teams = [
        Team(
            name="Justice League",
            headquarters="Gotham",
            heroes=[hero_batman, hero_superman, hero_flash],
        ),
        Team(name="Humanity", headquarters="Earth", heroes=[hero_cyborg, hero_flash]),
    ]
    for team in teams:
        session.add(team)
        session.commit()


def get_database_url() -> str:
    """
    Generate database URL from environment variables.
    Uses SQLite for testing, PostgreSQL for production.

    Returns:
        str: The database URL.
    """
    # Check if we're in test mode
    if os.getenv("TESTING", "false").lower() == "true":
        return "sqlite:///./test.db"

    # Get database configuration from environment variables for PostgreSQL
    db_user = os.getenv("POSTGRES_USER", "fastapi")
    db_password = os.getenv("POSTGRES_PASSWORD", "fastapi")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "fastapi_crud")

    # Return PostgreSQL database URL
    return f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def get_engine(db_url: str) -> Engine:
    """Create and return a new SQLAlchemy engine using the provided database URL.

    Args:
        db_url (str): The database URL to connect to.

    Returns:
        Engine: A SQLAlchemy Engine instance connected to the specified database.
    """
    # Add connect_args for SQLite to handle threading
    connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
    return create_engine(url=db_url, echo=True, connect_args=connect_args)


@contextmanager
def get_session(engine: Engine) -> Generator[Session, None, None]:
    """
    Context manager that yields a new Session object bound to the provided engine.

    Args:
        engine (Engine): The SQLAlchemy Engine instance to bind the session to.

    Yields:
        Session: A SQLModel Session instance.
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def create_db_and_tables(engine: Engine, models=None):
    """
    Create tables in the database using the provided engine and models.

    Args:
        engine (Engine): The SQLAlchemy Engine instance to use for table creation.
        models (list, optional): List of SQLModel classes to create tables for.
                               If None, uses all registered models.
    """
    if models:
        # Create only the specified models
        SQLModel.metadata.create_all(
            engine, tables=[model.__table__ for model in models]
        )
    else:
        # Create all models
        SQLModel.metadata.create_all(engine)


db_url = get_database_url()
engine = get_engine(db_url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables(engine)
    init_db(Session(engine))
    yield
