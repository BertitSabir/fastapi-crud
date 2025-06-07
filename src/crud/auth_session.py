from sqlmodel import Session, select

from src.crud.user import AuthSessionNotFoundError
from src.models.auth_session import AuthSession, AuthSessionCreate


def create_auth_session(
    auth_session: AuthSessionCreate,
    session: Session,
) -> AuthSession:
    db_auth_session = AuthSession.model_validate(auth_session)
    session.add(db_auth_session)
    session.commit()
    session.refresh(db_auth_session)
    return db_auth_session


def get_session_by_id(session_id: str, session: Session) -> AuthSession:
    auth_session = session.get(AuthSession, session_id)
    if not auth_session:
        message = f"AuthSession with id: {session_id} not found"
        raise AuthSessionNotFoundError(message)
    return auth_session


def get_session_by_user_id(user_id: str, session: Session) -> AuthSession:
    auth_session = session.exec(
        select(AuthSession).where(AuthSession.user_id == user_id),
    ).first()
    if not auth_session:
        message = f"AuthSession with user_id: {user_id} not found"
        raise AuthSessionNotFoundError(message)
    return auth_session
