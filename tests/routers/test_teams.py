def test_create_team(client):
    # Arrange
    team_data = {"name": "Avengers", "headquarters": "Earth"}

    # Act
    response = client.post(url="/teams/", json=team_data)
    data = response.json()

    # Assert
    assert response.status_code == 201
    assert data["name"] == team_data["name"]
    assert data["headquarters"] == team_data["headquarters"]
    assert data["id"] is not None


def test_list_teams(client):
    # Arrange:
    offset = 0
    limit = 1

    # Act:
    response = client.get("/teams/", params={"offset": offset, "limit": limit})

    # Assert
    assert response.status_code == 200


def test_get_existing_team_by_id(client):
    # Arrange:
    team_id = 1

    # Act:
    response = client.get(f"/teams/{team_id}")

    # Assert
    assert response.status_code == 200


def test_get_unexisting_team_by_id(client):
    # Arrange:
    team_id = 111111

    # Act:
    response = client.get(f"/teams/{team_id}")

    # Assert
    assert response.status_code == 404


def test_update_existing_team(client):
    # Arrange
    team_id = 1
    team_data = {"name": "Shazam", "secret_name": "Billy Batson", "age": 15}

    # Act
    response = client.patch(url=f"/teams/{team_id}", json=team_data)

    # Assert
    assert response.status_code == 200


def test_update_unexisting_team(client):
    # Arrange
    team_id = 0

    # Act
    response = client.patch(url=f"/teams/{team_id}", json={})

    # Assert
    assert response.status_code == 404


def test_delete_existing_team(client):
    # Arrange
    team_id = 1

    # Act
    response = client.delete(url=f"/teams/{team_id}")

    # Assert
    assert response.status_code == 204


def test_delete_unexisting_team(client):
    # Arrange
    team_id = 0

    # Act
    response = client.delete(url=f"/teams/{team_id}")

    # Assert
    assert response.status_code == 404
