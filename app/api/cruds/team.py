from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import team_member_settings

from ..models import TeamMember


async def get_team_member_by_id(db: AsyncSession, team_member_id: int) -> TeamMember:
    results = await db.execute(select(TeamMember).where(TeamMember.id == team_member_id))
    return results.scalars().first()


async def get_all_active_team_members(db: AsyncSession) -> list[TeamMember]:
    results = await db.execute(select(TeamMember).where(TeamMember.status == team_member_settings.PRESENT_STATUS))
    return results.scalars().all()


async def get_all_inactive_team_members(db: AsyncSession) -> list[TeamMember]:
    results = await db.execute(
        select(TeamMember).where(
            TeamMember.status == team_member_settings.PAST_STATUS
            )
        )
    return results.scalars.all()