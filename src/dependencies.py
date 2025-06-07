from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from src.database import engine


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]
