from sqlalchemy.ext.asyncio import AsyncSession

from app.config import transactions

from ..cruds import store as crud
from ..dependecies.exceptions import CategoryNotFound, EmptyObject
from ..schemas.store import CreateStoreItem, StoreItem
from ..schemas.user import User
from ..services.users_service import check_user_permission


async def get_all_store_items(db: AsyncSession, limit: int, 
                              offset: int) -> list[StoreItem]:
    items = await crud.get_all_store_items(db, limit=limit, offset=offset)
    return [StoreItem.model_validate(item) for item in items]


async def create_store_item(db: AsyncSession, store_item: CreateStoreItem,
                            current_user: User):
    await check_user_permission(current_user, transactions.CREATE_STORE_ITEM)
    
    available_sizes = await crud.get_all_sizes(db)
    available_sizes = [size.name for size in available_sizes]
    
    sizes = list(filter(lambda x: x not in available_sizes, store_item.sizes))
    
    if len(sizes) == 0:
        raise EmptyObject
    
    category_obj = await crud.get_category_by_name(
        db, name=store_item.category_name
    )
    if category_obj is None:
        raise CategoryNotFound
    
    
    