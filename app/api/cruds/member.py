from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import team_member_settings

from ..models import TeamMember


async def get_team_member_by_id(db: AsyncSession, team_member_id: int) -> TeamMember:
    results = await db.execute(select(TeamMember).where(TeamMember.id == team_member_id))
    return results.scalars().first()


async def get_all_active_team_members(db: AsyncSession) -> list[TeamMember]:
    results = await db.execute(
        select(TeamMember).
        where(TeamMember.status == team_member_settings.PRESENT_STATUS)
    )
    return results.scalars().all()


async def get_all_inactive_team_members(db: AsyncSession) -> list[TeamMember]:
    results = await db.execute(
        select(TeamMember).where(
                TeamMember.status == team_member_settings.PAST_STATUS
            )
        )
    return results.scalars.all()


async def add_team_member(db: AsyncSession, user_id: int, position: str, 
                          height: int | None, weight: int | None, 
                          status: str, role: str) -> TeamMember:
    new_member = TeamMember(
        user_id=user_id, status=status, role=role, position=position.lower(), 
        height=height, weight=weight
    )
    db.add(new_member)
    await db.commit()
    await db.refresh(new_member)
    
    return new_member


async def edit_team_member(db: AsyncSession, member: TeamMember, user_id: int, 
                           position: str, height: int | None, 
                           weight: int | None, status: str, 
                           role: str) -> TeamMember:
    member.user_id = user_id
    member.position = position
    member.height = height
    member.weight = weight
    member.status = status
    member.role = role
    await db.commit()
    await db.refresh(member)
    return member


async def delete_team_member(db: AsyncSession, member: TeamMember):
    await db.delete(member)
    await db.commit()