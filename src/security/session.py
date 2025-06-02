from sqlmodel import Session

from src.crud.user import get_user_by_email
from src.models.user import User
from src.security.utils import verify_password


def authenticate_user(
    email: str,
    plain_password: str,
    session: Session,
) -> User:
    db_user = get_user_by_email(email=email, session=session)
    if not db_user:
        return False
    if not verify_password(
        plain_password=plain_password,
        hashed_password=db_user.password,
    ):
        return False
    return db_user
