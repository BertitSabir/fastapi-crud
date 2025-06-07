from sqlmodel import Session, col, select

from src.models.user import User, UserCreate
from src.security.utils import get_password_hash


class UserNotFoundError(Exception):
    """Exception raised when a specified user cannot be found."""


class AuthSessionNotFoundError(Exception):
    """Exception raised when a specified AuthSession cannot be found."""


def create_user(user: UserCreate, session: Session) -> User:
    """
    Create a team in the database.

    Args:
        user (UserCreate): Data required to create a new team.
        session (Session): The database session used for operations.

    Returns:
        User: The newly created and saved user instance.

    """
    extra_data = {}
    user_data = user.model_dump(exclude_unset=True)
    if "password" in user_data:
        hashed_password = get_password_hash(plain_password=user_data["password"])
        extra_data = {"password": hashed_password}
    db_user = User.model_validate(user, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_id(*, user_id: int, session: Session) -> User:
    """
    Retrieve a user by its ID.

    Args:
        user_id (int): The unique identifier of the user to retrieve.
        session (Session): The database session used for operations.

    Returns:
        User: The retrieved user object.

    Raises:
        UserNotFoundError: If no user is found with the given identifier.

    """
    user = session.get(User, user_id)
    if not user:
        message = f"User with id: {user_id} not found"
        raise UserNotFoundError(message)
    return user


def get_user_by_username(*, username: str, session: Session) -> User:
    """
    Retrieve a user by its ID.

    Args:
        username (tsr): The unique identifier of the user to retrieve.
        session (Session): The database session used for operations.

    Returns:
        User: The retrieved user object.

    Raises:
        UserNotFoundError: If no user is found with the given identifier.

    """
    statement = select(User).where(col(User.username) == username)
    user = session.exec(statement).first()
    if not user:
        message = f"User with username: {username} not found"
        raise UserNotFoundError(message)
    return user


def get_user_by_email(*, email: str, session: Session) -> User:
    """
    Retrieve a user by its ID.

    Args:
        email (tsr): The unique identifier of the user to retrieve.
        session (Session): The database session used for operations.

    Returns:
        User: The retrieved user object.

    Raises:
        UserNotFoundError: If no user is found with the given identifier.

    """
    statement = select(User).where(col(User.email) == email)
    user = session.exec(statement).first()
    if not user:
        message = f"User with email: {email} not found"
        raise UserNotFoundError(message)
    return user
