from contextlib import asynccontextmanager, contextmanager
from typing import Generator

from fastapi import FastAPI
from sqlalchemy import create_engine, Engine
from sqlmodel import Session, SQLModel, text
from pathlib import Path

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
        Team(
            name="Humanity",
            headquarters="Earth",
            heroes=[hero_cyborg, hero_flash]
        )
    ]
    for team in teams:
        session.add(team)
        session.commit()


def get_database_url(name: str) -> str:
    """
    Generate an SQLite database URL string for the given database name.

    Args:
        name (str): The name of the database.

    Returns:
        str: The SQLite database URL.
    """
    # check if a databse with this name exist in the current directory
    if Path(f"{name}.db").exists():
        print(f"Database {name}.db already exists. Deleting it.")
        Path(f"{name}.db").unlink()
    # return the SQLite database URL
    return f"sqlite:///{name}.db"


def get_engine(db_url: str) -> Engine:
    """Create and return a new SQLAlchemy engine using the provided database URL.

    Args:
        db_url (str): The database URL to connect to.

    Returns:
        Engine: A SQLAlchemy Engine instance connected to the specified database.
    """
    return create_engine(url=db_url, echo=True)


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

    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))


db_url = get_database_url(name="crud")
engine = get_engine(db_url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables(engine)
    init_db(Session(engine))
    yield
