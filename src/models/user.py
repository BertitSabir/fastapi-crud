from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(unique=True)
    full_name: str = Field(index=True)
    email: EmailStr = Field(unique=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    verified: bool = False
    password: str


class UserCreate(UserBase):
    password: str = ...


class UserUpdate(UserCreate):
    username: str | None = None
    full_name: str | None = None
    password: str | None = None
