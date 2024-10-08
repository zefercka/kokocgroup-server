from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Permission


async def get_permission(db: AsyncSession, permission: str):
    results = await db.execute(select(Permission).where(Permission.name == permission))
    return results.scalars().first()