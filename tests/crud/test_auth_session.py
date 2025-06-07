import pytest
from faker import Faker

from src.crud.auth_session import (
    create_auth_session,
    get_session_by_id,
    get_session_by_user_id,
)
from src.crud.user import AuthSessionNotFoundError, create_user
from src.models.auth_session import AuthSessionCreate
from src.models.user import UserCreate

fake = Faker()


@pytest.fixture(name="user")
def user_fixture(session):
    # Arrange
    user_create = UserCreate(
        username=fake.user_name(),
        full_name=fake.name(),
        email=fake.email(),
        password=fake.password(),
    )
    user = create_user(user=user_create, session=session)
    return user


@pytest.fixture(name="auth_session")
def auth_session_fixture(session, user):
    auth_session = create_auth_session(
        auth_session=AuthSessionCreate(user_id=user.id),
        session=session,
    )
    return auth_session


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
