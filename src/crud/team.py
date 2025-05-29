from sqlmodel import Session, select
from src.models.team import TeamCreate, Team, TeamUpdate


class TeamNotFoundError(Exception):
    """
    Exception raised when a specified team cannot be found.
    """

    pass


def create_team(team: TeamCreate, session: Session) -> Team:
    """
    Create a team in the database.

    Args:
        team (TeamCreate): Data required to create a new team.
        session (Session): The database session used for operations.

    Returns:
        Team: The newly created and saved team instance.
    """
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


def get_teams(*, offset: int = 0, limit: int = 100, session: Session) -> list[Team]:
    """
    Retrieve teams from the database.

    Args:
        offset (int, optional): The number of records to skip, default is 0.
        limit (int, optional): The maximum number of records to retrieve, default is 100.
        session (Session): The database session to execute queries.

    Returns:
        list[Team]: A list of retrieved team objects.
    """
    statement = select(Team).offset(offset).limit(limit)
    return session.exec(statement).all()


def get_team_by_id(*, team_id: int, session: Session) -> Team:
    """
    Retrieve a team by its ID.

    Args:
        team_id (int): The unique identifier of the team to retrieve.
        session (Session): The database session used for operations.

    Returns:
        Team: The retrieved team object.

    Raises:
        TeamNotFoundError: If no team is found with the given identifier.
    """
    team = session.get(Team, team_id)
    if not team:
        raise TeamNotFoundError(f"Team with id: {team_id} not found")
    return team


def update_team(*, team_id: int, team: TeamUpdate, session: Session) -> Team:
    """
    Update a team by its ID.

    Args:
        team_id (int): The unique identifier of the team to update.
        team (TeamUpdate): An object containing updated team data.
        session (Session): The database session used to update records.

    Returns:
        Team: The updated team object.
    """
    db_team = get_team_by_id(team_id=team_id, session=session)
    team_data = team.model_dump(exclude_unset=True)
    db_team.sqlmodel_update(team_data)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


def delete_team(*, team_id: int, session: Session) -> bool:
    """
    Delete a team by its ID.

    Args:
        team_id (int): The unique identifier of the team to delete.
        session (Session): The database session to perform the deletion.

    Returns:
        bool: True if the team was successfully deleted.
    """
    db_team = get_team_by_id(team_id=team_id, session=session)
    session.delete(db_team)
    session.commit()
    return True
