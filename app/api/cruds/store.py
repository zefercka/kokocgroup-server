from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import StoreItem


async def get_all_store_items(db: AsyncSession, limit: int, offset: int):
    results = await db.execute(
        select(StoreItem).order_by(StoreItem.id).limit(limit).offset(offset)
    )
    return results.scalars().all()
