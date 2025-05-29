def test_create_hero(client):
    # Arrange
    hero_data = {"name": "Deadpool", "secret_name": "Dive Wilson"}

    # Act
    response = client.post(url="/heroes/", json=hero_data)
    result = response.json()

    # Assert
    assert response.status_code == 201
    assert result["name"] == hero_data["name"]
    assert result["secret_name"] == hero_data["secret_name"]
    assert result["age"] is None
    assert result["id"] is not None
    assert result["team_id"] is None
    assert "hashed_password" not in result


def test_list_heroes(client):
    # Arrange:
    offset = 0
    limit = 1
    expected_data = [
        {
            "name": "Batman",
            "secret_name": "Bruce Wayne",
            "age": 35,
            "team_id": 1,
            "id": 1,
            "team": {"name": "Justice League", "headquarters": "Gotham", "id": 1},
        }
    ]

    # Act:
    response = client.get("/heroes/", params={"offset": offset, "limit": limit})
    gotten_data = response.json()

    # Assert
    assert response.status_code == 200
    assert gotten_data == expected_data


def test_get_existing_hero_by_id(client):
    # Arrange:
    hero_id = 1

    # Act:
    response = client.get(f"/heroes/{hero_id}")

    # Assert
    assert response.status_code == 200


def test_get_unexisting_hero_by_id(client):
    # Arrange:
    hero_id = 111111

    # Act:
    response = client.get(f"/heroes/{hero_id}")

    # Assert
    assert response.status_code == 404


def test_update_existing_hero(client):
    # Arrange
    hero_id = 1
    hero_data = {"name": "Shazam", "secret_name": "Billy Batson", "age": 15}

    # Act
    response = client.patch(url=f"/heroes/{hero_id}", json=hero_data)
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["name"] == hero_data["name"]


def test_update_unexisting_hero(client):
    # Arrange
    hero_id = 0

    # Act
    response = client.patch(url=f"/heroes/{hero_id}", json={})

    # Assert
    assert response.status_code == 404


def test_delete_existing_hero(client):
    # Arrange
    hero_id = 1

    # Act
    response = client.delete(url=f"/heroes/{hero_id}")

    # Assert
    assert response.status_code == 204


def test_delete_unexisting_hero(client):
    # Arrange
    hero_id = 0

    # Act
    response = client.delete(url=f"/heroes/{hero_id}")

    # Assert
    assert response.status_code == 404
