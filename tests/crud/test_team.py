import pytest

from src.crud.team import (
    TeamNotFoundError,
    create_team,
    delete_team,
    get_team_by_id,
    get_teams,
    update_team,
)
from src.models.team import Team, TeamCreate, TeamUpdate


def test_create_team(session):
    # Arrange
    team = TeamCreate(
        name="Avengers",
        headquarters="LA",
    )

    # Act
    gotten = create_team(team, session)

    # Assert
    gotten.name = team.name
    gotten.headquarters = team.headquarters


def test_get_teams(session, team_avengers_is_here):  # noqa: ARG001
    # Act
    teams = get_teams(offset=0, limit=1, session=session)

    # Assert
    assert len(teams) == 1
    assert isinstance(teams, list)


def test_get_existing_team_by_id(session, team_avengers_is_here):  # noqa: ARG001
    # Arrange
    team_id = 1

    # Act
    gotten_team = get_team_by_id(team_id=1, session=session)

    # Assert
    assert gotten_team.id == team_id
    assert isinstance(gotten_team, Team)


def test_get_unexisting_team_by_id(session):
    # Arrange
    team_id = 0

    # Act & Assert
    with pytest.raises(TeamNotFoundError):
        get_team_by_id(team_id=team_id, session=session)


def test_update_team(session, team_avengers_is_here):
    # Arrange
    team_id = team_avengers_is_here.id
    team = TeamUpdate(name="Homeless", headquarters=None)

    # Act
    gotten_team = update_team(team_id=team_id, team=team, session=session)

    # Assert
    assert gotten_team.name == "Homeless"
    assert gotten_team.headquarters is None


def test_delete_team(session, team_avengers_is_here):
    # Arrange
    team_id = team_avengers_is_here.id

    # Act
    deleted = delete_team(team_id=team_id, session=session)

    # Assert
    assert deleted
    with pytest.raises(TeamNotFoundError):
        get_team_by_id(team_id=team_id, session=session)
