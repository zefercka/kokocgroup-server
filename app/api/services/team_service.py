from sqlalchemy.ext.asyncio import AsyncSession

from app.config import team_member_settings, transactions

from ..cruds import team as crud
from ..dependecies.exceptions import NoPermissions, MemberNotFound
from ..models import TeamMember
from ..schemas.team import Member, NewMember, Team, EditMember
from ..schemas.user import User
from ..services.user_service import check_user_permission, get_user


async def get_all_active_team_members(db: AsyncSession):
    members = await crud.get_all_active_team_members(db)
    team = await validate_team_model(members=members)
    
    return team


async def get_all_inactive_team_members(db: AsyncSession):
    members = await crud.get_all_inactive_team_members(db)
    team = await validate_team_model(members=members)
    
    return team


async def validate_member_model(member: TeamMember) -> Member:
    validated_member = Member.model_validate(member)
    validated_member.first_name = member.user.first_name
    validated_member.last_name = member.user.last_name
    validated_member.date_of_birth = member.user.date_of_birth
    validated_member.avatar_url = member.user.avatar_url
    
    return validated_member


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
        validated_member = await validate_member_model(member)
        
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
            
    
async def add_team_member(db: AsyncSession, member: NewMember, 
                          current_user: User) -> Member:
    if not await check_user_permission(
        current_user, transactions.ADD_TEAM_MEMBER
    ):
        raise NoPermissions
    
    if member.user_id != None:
        # Вызовет исключение, если юзера нет
        await get_user(db, member.user_id)
    
    member = await crud.add_team_member(db, **member.model_dump())
    member = await validate_member_model(member)
    return member


async def edit_team_member(db: AsyncSession, member: EditMember, 
                           current_user: User) -> Member:
    if not await check_user_permission(
        current_user, transactions.EDIT_TEAM_MEMBER
    ):
        raise NoPermissions
    
    member_obj = await crud.get_team_member_by_id(
        db, team_member_id=member.id
    )
    if member_obj is None:
        raise MemberNotFound
    
    if member.user_id != member_obj.user_id:
        # Вызовет исключение, если юзера нет
        await get_user(db, member.user_id)
        
    member = await crud.edit_team_member(
        db, member=member_obj, 
        **member.model_dump(exclude=["id", "role", "status"]),
        role=member.role.value, status=member.status.value
    )
    member = await validate_member_model(member)
    return member