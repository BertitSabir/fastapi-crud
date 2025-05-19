
from typing import Annotated
from sqlmodel import Session
from fastapi import Depends

from db import engine


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
