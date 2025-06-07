import logging

from fastapi import status

logger = logging.getLogger(__name__)


def test_create_user(client, fake):
    # Arrange
    user_data = {
        "username": fake.user_name(),
        "full_name": fake.name(),
        "email": fake.email(),
        "password": fake.password(),
    }

    # Act
    response = client.post(url="/users/", json=user_data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED


def test_get_login_form(client):
    # Act
    response = client.get(url="/users/login")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]


def test_login_user_with_valid_credentials(client, user, test_password):
    # Act
    response = client.post(
        url="/users/login",
        data={
            "email": user.email,
            "password": test_password,
        },
        follow_redirects=False,
    )

    # Assert
    assert response.status_code == status.HTTP_302_FOUND

    response = client.get("/users/home")
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]

    response = client.get("/users/profile")
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]

    response = client.get("/users/logout", follow_redirects=False)
    assert response.status_code == status.HTTP_302_FOUND


def test_login_user_with_bad_credentials(client, user):
    # Act
    response = client.post(
        url="/users/login",
        data={
            "email": user.email,
            "password": "bad_password",
        },
        follow_redirects=False,
    )

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
