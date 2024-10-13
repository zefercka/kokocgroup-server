from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import BaseSettings
from loguru import logger


@logger.catch
async def get_settings(db: AsyncSession, name: str):
    results = await db.execute(
        select(BaseSettings).where(BaseSettings.name == name)
    )
    return results.scalars().first()