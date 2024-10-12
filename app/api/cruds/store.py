from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import StoreItem, Size, StoreCategory

async def get_all_store_items(db: AsyncSession, limit: int, 
                              offset: int, filter: str,
                              category_name: str) -> list[StoreItem]:
    query = (select(StoreItem))
    
    if filter == "new":
        query = query.order_by(StoreItem.created_at.desc())
    elif filter == "expensive":
        query = query.order_by(StoreItem.price.desc())
    elif filter == "cheap":
        query = query.order_by(StoreItem.price.asc())
    else:
        query = query.order_by(StoreItem.id)
    
    if category_name:
        query = query.where(StoreItem.category_name == category_name)
    
    query = query.limit(limit).offset(offset)
    
    results = await db.execute(query)
    return results.scalars().all()


async def get_all_sizes(db: AsyncSession) -> list[Size]:
    results = await db.execute(select(Size))
    return results.scalars().all()


async def get_sizes(db: AsyncSession, sizes: list[str]):
    results = await db.execute(
        select(Size).where(Size.size.in_(sizes))   
    )
    return results.scalars().all()


async def get_category_by_name(db: AsyncSession, name: str) -> StoreCategory:
    results = await db.execute(
        select(StoreCategory).where(StoreCategory.name == name)    
    )
    return results.scalars().first()


async def create_store_item(db: AsyncSession, title: str, price: int, 
                            description: str, category_name: str, 
                            image_url: str, sizes: list[Size]) -> StoreItem:
    store_item = StoreItem(
        title=title, price=price, description=description, 
        category_name=category_name, image_url=image_url, sizes=sizes
    )
    db.add(store_item)
    await db.commit()
    await db.refresh(store_item)
    
    return store_item


async def update_store_item(db: AsyncSession, store_item: StoreItem, 
                            title: str, price: str, description: str, 
                            category_name: str, image_url: str,
                            sizes: list[Size]) -> StoreItem:
    store_item.title = title
    store_item.price = price
    store_item.description = description
    store_item.category_name = category_name
    store_item.image_url = image_url
    store_item.sizes = sizes
    await db.commit()
    await db.refresh(store_item)
    
    return store_item


async def get_store_item_by_id(db: AsyncSession, 
                               store_item_id: int) -> StoreItem:
    results = await db.execute(
        select(StoreItem).where(StoreItem.id == store_item_id)
    )
    return results.scalars().first()


async def delete_store_item(db: AsyncSession, store_item: StoreItem):
    await db.delete(store_item)
    await db.commit()
    

async def get_all_store_categories(db: AsyncSession, limit: int, 
                                   offset: int) -> list[StoreCategory]:
    results = await db.execute(
        select(StoreCategory).offset(offset).limit(limit)
    )
    return results.scalars().all()