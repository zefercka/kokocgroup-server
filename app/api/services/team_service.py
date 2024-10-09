from sqlalchemy.ext.asyncio import AsyncSession

from ..cruds import team as crud
from ..schemas.team import Team, Member
from ..models import TeamMember
from app.config import team_member_settings
import time


async def get_all_active_team_members(db: AsyncSession):
    members = await crud.get_all_active_team_members(db)
    team = await validate_team_model(members=members)
    
    return team


async def get_all_inactive_team_members(db: AsyncSession):
    members = await crud.get_all_inactive_team_members(db)
    team = await validate_team_model(members=members)
    
    return team


async def validate_team_model(members: list[TeamMember]) -> Team:
    team_members: dict[str, list[Member]] = {
        "trainers": [],
        "goalkeepers": [],
        "defenders": [],
        "midfielders": [],
        "strikers": [],
        "admins": [],
    }

    for member in members:
        validated_member = Member.model_validate(member)
        validated_member.first_name = member.user.first_name
        validated_member.last_name = member.user.last_name
        validated_member.date_of_birth = member.user.date_of_birth
        validated_member.avatar_url = member.user.avatar_url
        
        if member.role == team_member_settings.ADMIN_ROLE:
            team_members["admins"].append(validated_member)
        elif member.role == team_member_settings.TRAINER_ROLE:
            team_members["trainers"].append(validated_member)
        elif member.role == team_member_settings.PLAYER_ROLE:
            if member.position == team_member_settings.GOALKEPPER_POSITION:
                team_members["goalkeepers"].append(validated_member)
            elif member.position == team_member_settings.DEFENDER_POSITION:
                team_members["defenders"].append(validated_member)
            elif member.position == team_member_settings.MIDFIELDERS_POSITION:
                team_members["midfielders"].append(validated_member)
            elif member.position == team_member_settings.STRIKER_POSITION:
                team_members["strikers"].append(validated_member)
    
    team = Team(**team_members)

    return team            
            
    