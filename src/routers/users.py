import functools
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_302_FOUND
from starlette.templating import Jinja2Templates

from src.crud.auth_session import create_auth_session, get_session_by_id
from src.crud.user import AuthSessionNotFoundError, create_user
from src.dependencies import SessionDep
from src.models.auth_session import AuthSessionCreate
from src.models.public import UserPublic
from src.models.user import User, UserCreate
from src.security.session import authenticate_user

templates_path = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=templates_path)

router = APIRouter(prefix="/users", tags=["Users"])


def login_required(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        session = kwargs.get("session")
        session_id = request.session.get("session_id")

        if not session_id:
            raise HTTPException(
                status_code=HTTP_302_FOUND,
                headers={"Location": "/users/login"},
            )

        try:
            auth_session = get_session_by_id(session_id=session_id, session=session)
        except AuthSessionNotFoundError as e:
            raise HTTPException(
                status_code=HTTP_302_FOUND,
                headers={"Location": "/users/login"},
            ) from e

        if auth_session and auth_session.expired:
            raise HTTPException(
                status_code=HTTP_302_FOUND,
                headers={"Location": "/users/login"},
            )

        request.state.user = auth_session.user

        return await func(*args, **kwargs)

    return wrapper


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create(user: UserCreate, session: SessionDep) -> User:
    return create_user(user, session)


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login(
    *,
    request: Request,
    email: Annotated[str, Form()] = ...,
    password: Annotated[str, Form()] = ...,
    session: SessionDep,
):
    user = authenticate_user(email=email, plain_password=password, session=session)
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"},
        )
    auth_session = create_auth_session(AuthSessionCreate(user_id=user.id), session)
    request.session["user_id"] = user.id
    request.session["session_id"] = auth_session.id
    request.state.user = user
    response = RedirectResponse("/users/home", status_code=HTTP_302_FOUND)
    return response


@router.get("/home", response_class=HTMLResponse)
@login_required
async def homepage(
    request: Request,
    session: SessionDep,  # noqa: ARG001
):
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "user": request.state.user},
    )


@router.get("/profile", response_class=HTMLResponse)
@login_required
async def profile(
    request: Request,
    session: SessionDep,  # noqa: ARG001
):
    user = request.state.user
    user_profile = UserPublic(**user.model_dump())
    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "user": user_profile},
    )


@router.get("/logout", status_code=status.HTTP_302_FOUND)
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/users/login", status_code=HTTP_302_FOUND)
