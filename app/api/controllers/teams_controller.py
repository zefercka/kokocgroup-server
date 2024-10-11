from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependecies.database import get_db
from ..schemas.team import Team, NewMember, EditMember, TeamList
from ..schemas.user import User
from ..services import auth_service, team_service
from app.config import team_member_settings

app = APIRouter()


@app.get("", response_model=TeamList)
async def get_team_members(status: str = "present", db: AsyncSession = Depends(get_db)):
    if status == team_member_settings.PRESENT_STATUS:
        members = await team_service.get_all_active_team_members(db)
    elif status == team_member_settings.PAST_STATUS:
        members = await team_service.get_all_inactive_team_members(db)
    else:
        members = []   
            
    return members


@app.post("")
async def add_team_member(member: NewMember, 
                          current_user: User = Depends(auth_service.get_current_user),
                          db: AsyncSession = Depends(get_db)):
    member = await team_service.add_team_member(
        db, member=member, current_user=current_user
    )
    return member


@app.put("")
async def edit_team_member(member: EditMember,
                           current_user: User = Depends(auth_service.get_current_user),
                           db: AsyncSession = Depends(get_db)):
    member = await team_service.edit_team_member(
        db, member=member, current_user=current_user
    )
    

@app.delete("/{member_id}")
async def delete_team_member(member_id: int, 
                             current_user: User = Depends(auth_service.get_current_user),
                             db: AsyncSession = Depends(get_db)):
    await team_service.delete_team_member(
        db, current_user=current_user, member_id=member_id
    )