from fastapi import FastAPI

from src.database import lifespan
from src.routers import heroes, teams, users

# Create FastAPI app:
app = FastAPI(lifespan=lifespan)


app.include_router(heroes.router)
app.include_router(teams.router)
app.include_router(users.router)
