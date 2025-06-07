import pytest

from src.crud.auth_session import (
    get_session_by_id,
    get_session_by_user_id,
)
from src.crud.user import AuthSessionNotFoundError


def test_create_auth_session(auth_session):
    # Assert
    assert isinstance(auth_session.id, str)
    assert auth_session.active
    assert not auth_session.expired


def test_get_existing_auth_session_by_user_id(session, auth_session):
    # Act
    gotten_auth_session = get_session_by_user_id(
        user_id=auth_session.user_id,
        session=session,
    )

    # Assert
    assert gotten_auth_session.user == auth_session.user


def test_get_unexisting_auth_session_by_user_id(session):
    # Act & Assert
    with pytest.raises(AuthSessionNotFoundError):
        get_session_by_user_id(
            user_id=0,
            session=session,
        )


def test_get_unexisting_auth_session_by_id(session):
    # Act & Assert
    with pytest.raises(AuthSessionNotFoundError):
        get_session_by_id(
            session_id=0,
            session=session,
        )


def test_get_auth_session_by_id(session, auth_session):
    # Act
    gotten_auth_session = get_session_by_id(
        session_id=auth_session.id,
        session=session,
    )

    # Assert
    assert gotten_auth_session.id == auth_session.id
