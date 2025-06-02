import os

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from src.database import lifespan
from src.routers import heroes, teams, users

# Create FastAPI app:
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("SESSION_SECRET_KEY", "supersecret"),
)


app.include_router(heroes.router)
app.include_router(teams.router)
app.include_router(users.router)
