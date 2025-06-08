import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.crud.user import (
    UserAlreadyExistsError,
    UserNotFoundError,
    create_user,
    get_user_by_username,
    get_users,
)
from src.dependencies import (
    OAuth2PasswordBearerDep,
    OAuth2PasswordRequestFormDep,
    SessionDep,
)
from src.models.public import UserPublic
from src.models.user import User, UserCreate, UserLogin
from src.security.utils import verify_password

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


logger = logging.getLogger(__name__)


async def get_current_user(token: OAuth2PasswordBearerDep, session: SessionDep):
    logger.info("toke: %s", token)
    try:
        user = get_user_by_username(username=token, session=session)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    else:
        return user


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
    offset: Annotated[int, Query(...)] = 0,
    limit: Annotated[int, Query(...)] = 100,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[User]:
    logger.info("current user: %s", current_user)
    return get_users(offset=offset, limit=limit, session=session)


@router.post("/token")
async def login(
    credentials: OAuth2PasswordRequestFormDep,
    session: SessionDep,
):
    validated_credentials = UserLogin(
        username=credentials.username,
        password=credentials.password,
    )
    try:
        user = get_user_by_username(
            username=validated_credentials.username,
            session=session,
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        ) from e
    if not verify_password(
        plain_password=credentials.password,
        hashed_password=user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )
    return {"access_token": user.username}
