from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db
from app.api.schemas.team import CreateTeam, Team
from app.api.schemas.user import User
from app.api.services import teams_service
from app.api.services.auth_service import get_current_user
from app.config import team_member_settings

app = APIRouter()


@app.get("", response_model=list[Team])
async def get_all_teams(limit: int = 10, offset: int = 0, 
                        db: AsyncSession = Depends(get_db)):
    teams = await teams_service.get_all_teams(
        db, limit=limit, offset=offset
    )
    return teams


@app.get("/{team_id}", response_model=Team)
async def get_team(team_id: int, db: AsyncSession = Depends(get_db)):
    team = await teams_service.get_team(db, team_id=team_id)
    return team


@app.post("", response_model=Team)
async def create_team(team: CreateTeam, 
                      current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    team = await teams_service.create_team(
        db, team=team, current_user=current_user
    )
    return team


@app.put("", response_model=Team)
async def edit_team(team: Team, current_user: User = Depends(get_current_user),
                    db: AsyncSession = Depends(get_db)):
    team = await teams_service.edit_team(
        db, team=team, current_user=current_user   
    )
    return team
    
    
@app.delete("/{team_id}")
async def delete_team(team_id: int, 
                      current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    await teams_service.delete_team(
        db, team_id=team_id, current_user=current_user
    )