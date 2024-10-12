from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.store import StoreItem, CreateStoreItem
from ..cruds import store as crud


async def get_all_store_items(db: AsyncSession, limit: int, 
                              offset: int) -> list[StoreItem]:

    items = await crud.get_all_store_items(db, limit=limit, offset=offset)
    return [StoreItem.model_validate(item) for item in items]


async def create_store_item(store_item: CreateStoreItem, db: AsyncSession)