from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import StoreItem, Size, StoreCategory

async def get_all_store_items(db: AsyncSession, limit: int, 
                              offset: int) -> list[StoreItem]:
    results = await db.execute(
        select(StoreItem).order_by(StoreItem.id).limit(limit).offset(offset)
    )
    return results.scalars().all()


async def get_all_sizes(db: AsyncSession) -> list[Size]:
    results = await db.execute(select(Size))
    return results.scalars().all()


async def get_sizes(db: AsyncSession, sizes: list[str]):
    results = await db.execute(
        select(Size).where(Size.size in sizes)   
    )
    return results.scalars().all()


async def get_category_by_name(db: AsyncSession, name: str) -> StoreCategory:
    results = await db.execute(
        select(StoreCategory).where(StoreCategory.name == name)    
    )
    return results.scalars().all()


async def create_store_item(db: AsyncSession, title: str, price: int, 
                            description: str, category_name: str, 
                            image_url: str, sizes: list[Size]) -> StoreItem:
    store_item = StoreItem(
        title=title, price=price, description=description, 
        category_name=category_name, image_url=image_url, sizes=sizes
    )