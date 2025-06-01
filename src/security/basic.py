import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

app = FastAPI()


security = HTTPBasic()


class User(BaseModel):
    username: str
    password: str


async def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    """Get the current user's username."""
    current_user = User(username="saber", password="password")  # noqa: S106
    user = User(username=credentials.username, password=credentials.password)
    current_username, current_password = (
        current_user.username.encode("utf-8"),
        current_user.password.encode("utf-8"),
    )
    username, password = user.username.encode("utf-8"), user.password.encode("utf-8")
    is_correct_username = secrets.compare_digest(current_username, username)
    is_correct_password = secrets.compare_digest(current_password, password)
    if not all((is_correct_username, is_correct_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return current_user.username


@app.get("/users/me")
async def read_current_user(
    username: Annotated[str, Depends(get_current_username)],
) -> str:
    return username
