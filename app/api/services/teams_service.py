from sqlalchemy.ext.asyncio import AsyncSession

from app.api.cruds import team as crud
from app.api.dependencies.exceptions import TeamNotFound
from app.api.schemas.team import CreateTeam, Team
from app.api.schemas.user import User
from app.api.services.users_service import check_user_permission
from app.config import transactions


async def get_team(db: AsyncSession, team_id: int) -> Team:
    team = await crud.get_team_by_id(db, team_id=team_id)
    
    if team is None:
        raise TeamNotFound
    
    return Team.model_validate(team)


async def get_all_teams(db: AsyncSession, limit: int, 
                        offset: int) -> list[Team]:
    team_objs = await crud.get_all_teams(
        db, limit=limit, offset=offset
    )
    teams = [Team.model_validate(team) for team in team_objs]
    return teams


async def create_team(db: AsyncSession, team: CreateTeam, 
                      current_user: User) -> Team:
    await check_user_permission(current_user, transactions.CREATE_TEAM)
    team = await crud.create_team(
        db, name=team.name, logo_url=team.logo_url
    )
    return Team.model_validate(team)
    

async def edit_team(db: AsyncSession, team: Team, current_user: User) -> Team:
    await check_user_permission(current_user, transactions.EDIT_TEAM)
    
    team_obj = await crud.get_team_by_id(db, team_id=team.id)
    if team_obj is None:
        raise TeamNotFound
        
    team = await crud.edit_team(
        db, team=team_obj, name=team.name, logo_url=team.logo_url
    )
    
    return Team.model_validate(team)


async def delete_team(db: AsyncSession, team_id: int, current_user: User):
    await check_user_permission(current_user, transactions.DELETE_TEAM)
    
    team_obj = await crud.get_team_by_id(db, team_id=team_id)
    if team_obj is None:
        raise TeamNotFound
    
    await crud.delete_team(db, team=team_obj)