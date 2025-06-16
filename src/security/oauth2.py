import logging
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from fastapi import HTTPException, status
from fastapi.security import SecurityScopes
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel, ValidationError
from sqlmodel import Session

from src.config.settings import settings
from src.crud.user import UserNotFoundError, get_user_by_username
from src.dependencies import OAuth2PasswordBearerDep, SessionDep
from src.models.user import User
from src.security.utils import verify_password

logger = logging.getLogger(__name__)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    scopes: list[str] = []


async def authenticate_user(username: str, password: str, session: Session) -> User:
    try:
        user = get_user_by_username(username=username, session=session)
    except UserNotFoundError:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> Token:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.secret_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes,
    token: OAuth2PasswordBearerDep,
    session: SessionDep,
):
    logger.info("Current user scopes: %s", security_scopes.scopes)
    if security_scopes.scopes:
        authenticate_value = f"Bearer scope={security_scopes.scope_str}"
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.secret_key,
            algorithms=[settings.algorithm],
        )
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        logger.info("token_scopes scopes: %s", token_scopes)
        token_data = TokenData(username=username, scopes=token_scopes)
    except (InvalidTokenError, ValidationError) as e:
        raise credentials_exception from e
    try:
        user = get_user_by_username(username=token_data.username, session=session)
    except UserNotFoundError as e:
        raise credentials_exception from e

    for scope in security_scopes.scopes:
        logger.info("ssssssssssssssssssssssssssssssscope: %s", scope)
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
