from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session

from src.database import engine


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

OAuth2PasswordBearerDep = Annotated[str, Depends(oauth2_scheme)]

OAuth2PasswordRequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
