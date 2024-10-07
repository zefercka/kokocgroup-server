from ..models import Permission
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_permission(db: AsyncSession, permission: str):
    results = await db.execute(select(Permission).where(Permission.name == permission))
    return results.scalars().first()