from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db
from app.api.dependencies.enums import MemberStatuses
from app.api.schemas.member import EditMember, NewMember, TeamList
from app.api.schemas.user import User
from app.api.services import auth_service, members_service

app = APIRouter()


@app.get("", response_model=TeamList)
async def get_team_members(status: MemberStatuses = MemberStatuses.PRESENT, 
                           db: AsyncSession = Depends(get_db)):
    if status == MemberStatuses.PRESENT:
        members = await members_service.get_all_active_team_members(db)
    elif status == MemberStatuses.PAST:
        members = await members_service.get_all_inactive_team_members(db)
            
    return members


@app.post("")
async def add_team_member(member: NewMember, 
                          current_user: User = Depends(auth_service.get_current_user),
                          db: AsyncSession = Depends(get_db)):
    member = await members_service.add_team_member(
        db, member=member, current_user=current_user
    )
    return member


@app.put("")
async def edit_team_member(member: EditMember,
                           current_user: User = Depends(auth_service.get_current_user),
                           db: AsyncSession = Depends(get_db)):
    member = await members_service.edit_team_member(
        db, member=member, current_user=current_user
    )
    

@app.delete("/{member_id}")
async def delete_team_member(member_id: int, 
                             current_user: User = Depends(auth_service.get_current_user),
                             db: AsyncSession = Depends(get_db)):
    await members_service.delete_team_member(
        db, current_user=current_user, member_id=member_id
    )