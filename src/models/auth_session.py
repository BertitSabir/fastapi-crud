import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.user import User

SESSION_TIMEOUT = 30


class AuthSession(SQLModel, table=True):
    __tablename__ = "auth_session"

    user_id: int = Field(foreign_key="user.id")
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.UTC),
        index=True,
    )
    active: bool = True

    user: "User" = Relationship(back_populates="auth_session")

    @property
    def expired(self) -> bool:
        right_now = datetime.datetime.now(tz=datetime.UTC)
        created_at = self.created_at
        if created_at.tzinfo is None:
            # Assume UTC if naive
            created_at = created_at.replace(tzinfo=datetime.UTC)
        return (right_now - created_at) > datetime.timedelta(
            seconds=SESSION_TIMEOUT,
        )


class AuthSessionCreate(SQLModel):
    user_id: int = ...
