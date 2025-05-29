from fastapi import FastAPI

from src.database import lifespan
from src.routers import heroes, teams

# Create FastAPI app:
app = FastAPI(lifespan=lifespan)  # noqa


app.include_router(heroes.router)
app.include_router(teams.router)