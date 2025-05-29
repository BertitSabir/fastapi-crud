from sqlmodel import Session, select
from src.models.team import TeamCreate, Team, TeamUpdate


class TeamNotFoundError(Exception):
    pass

def create_team(team: TeamCreate, session: Session) -> Team:
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


def get_teams(
    *,
    offset: int = 0,
    limit: int = 100,
    session: Session
) -> list[Team]:
    statement = select(Team).offset(offset).limit(limit)
    return session.exec(statement).all()


def get_team_by_id(
    *,
    team_id: int,
    session: Session
) -> Team:
    team = session.get(Team, team_id)
    if not team:
        raise TeamNotFoundError(f'Team with id: {team_id} not found')
    return team


def update_team(
    *,
    team_id: int,
    team: TeamUpdate,
    session: Session
) -> Team:
    db_team = get_team_by_id(team_id=team_id, session=session)
    team_data = team.model_dump(exclude_unset=True)
    # updates the in-memory object with new data
    db_team.sqlmodel_update(team_data)
    # persist session
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


def delete_team(
        *,
        team_id: int,
        session: Session
) -> bool:
    db_team = get_team_by_id(team_id=team_id, session=session)
    session.delete(db_team)
    session.commit()
    return True

