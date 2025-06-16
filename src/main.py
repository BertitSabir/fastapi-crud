from fastapi import FastAPI

from src.config.log_config import configure_logging
from src.database import lifespan
from src.routers import heroes, teams, users

configure_logging()
app = FastAPI(lifespan=lifespan)


app.include_router(heroes.router)
app.include_router(teams.router)
app.include_router(users.router)
