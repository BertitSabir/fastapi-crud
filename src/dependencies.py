from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlmodel import Session

from src.crud.auth_session import get_session_by_id
from src.crud.user import AuthSessionNotFoundError
from src.database import engine
from src.models.user import User


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(
    request: Request,
    session: SessionDep,
):
    session_id = request.session.get("session_id")

    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            headers={"Location": "/users/login"},
        )

    try:
        auth_session = get_session_by_id(session_id=session_id, session=session)
    except AuthSessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            headers={"Location": "/users/login"},
        ) from e

    if auth_session and auth_session.expired:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            headers={"Location": "/users/login"},
        )

    user = auth_session.user
    request.state.user = user

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
