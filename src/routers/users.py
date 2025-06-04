import logging
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.config.settings import settings
from src.crud.user import (
    UserAlreadyExistsError,
    create_user,
    get_users,
)
from src.dependencies import (
    OAuth2PasswordRequestFormDep,
    SessionDep,
)
from src.models.public import UserPublic
from src.models.user import User, UserCreate
from src.security.oauth2 import (
    Token,
    authenticate_user,
    create_access_token,
    get_current_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


logger = logging.getLogger(__name__)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create(user: UserCreate, session: SessionDep) -> User:
    try:
        return create_user(user, session)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        ) from e


@router.get("/", response_model=list[UserPublic])
async def list_users(
    *,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[User]:
    logger.info("current user: %s", current_user)
    return get_users(offset=offset, limit=limit, session=session)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    credentials: OAuth2PasswordRequestFormDep,
    session: SessionDep,
):
    user = await authenticate_user(
        username=credentials.username,
        password=credentials.password,
        session=session,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_toke_expires = timedelta(minutes=settings.access_token_expire_minutes)
    jwt = create_access_token(
        data={"sub": user.username},
        expires_delta=access_toke_expires,
    )
    return Token(access_token=jwt, token_type="bearer")  # noqa: S106
