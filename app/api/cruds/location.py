from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import team_member_settings

from ..models import Location


async def get_location_by_id(db: AsyncSession, location_id: int) -> Location:
    results = await db.execute(
        select(Location).where(Location.id == location_id)
    )
    return results.scalars().first()

