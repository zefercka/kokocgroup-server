from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import TeamMemberSettings

from ..models import TeamMember


async def get_team_member_by_id(db: AsyncSession, team_member_id: int) -> TeamMember:
    results = await db.execute(select(TeamMember).where(TeamMember.id == team_member_id))
    return results.scalars().first()


async def get_all_active_team_members(db: AsyncSession) -> list[TeamMember]:
    results = await db.execute(select(TeamMember).where(TeamMember.status == TeamMemberSettings.PRESENT_STATUS))
    return results.scalars().all()