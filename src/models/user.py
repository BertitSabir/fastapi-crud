from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(unique=True)
    full_name: str = Field(default=None, index=True)
    email: EmailStr = Field(default=None, index=True)
    active: bool = Field(default=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    verified: bool = False
    password: str


class UserCreate(UserBase):
    password: str = ...


class UserLogin(UserBase):
    username: str = ...
    password: str = ...
    full_name: str | None = None
    email: str | None = None
    active: bool | None = None


class UserUpdate(UserCreate):
    username: str | None = None
    full_name: str | None = None
    password: str | None = None
