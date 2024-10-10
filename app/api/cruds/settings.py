from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import BaseSettings


async def get_settings(db: AsyncSession, name: str):
    results = await db.execute(
        select(BaseSettings).where(BaseSettings.name == name)
    )
    return results.scalars().first()