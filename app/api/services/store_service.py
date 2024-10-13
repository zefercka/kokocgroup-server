from sqlalchemy.ext.asyncio import AsyncSession

from app.config import transactions

from ..cruds import store as crud
from ..dependecies.enums import StoreItemFilters
from ..dependecies.exceptions import (CategoryNotFound, EmptyObject,
                                      StoreItemNotFound)
from ..schemas.store import CreateStoreItem, StoreItem
from ..schemas.user import User
from ..services.users_service import check_user_permission


async def get_all_store_items(db: AsyncSession, limit: int, 
                              offset: int, filter: StoreItemFilters,
                              category: str | None) -> list[StoreItem]:
    items = await crud.get_all_store_items(
        db, limit=limit, offset=offset, category_name=category, filter=filter
    )
    return [StoreItem.model_validate(item) for item in items]


async def create_store_item(db: AsyncSession, store_item: CreateStoreItem,
                            current_user: User) -> StoreItem:
    await check_user_permission(current_user, transactions.CREATE_STORE_ITEM)
    
    sizes = await crud.get_sizes(db, sizes=store_item.sizes)
    if len(sizes) == 0:
        raise EmptyObject
    
    category_obj = await crud.get_category_by_name(
        db, name=store_item.category_name
    )
    if category_obj is None:
        raise CategoryNotFound
    
    store_item_obj = await crud.create_store_item(
        db, **store_item.model_dump(exclude=["sizes"]), sizes=sizes
    )
    return StoreItem.model_validate(store_item_obj)


async def edit_store_item(db: AsyncSession, store_item: StoreItem,
                          current_user: User) -> StoreItem:
    await check_user_permission(current_user, transactions.EDIT_STORE_ITEM)
    
    sizes = await crud.get_sizes(db, sizes=store_item.sizes)
    if len(sizes) == 0:
        raise EmptyObject
    
    category_obj = await crud.get_category_by_name(
        db, name=store_item.category_name
    )
    if category_obj is None:
        raise CategoryNotFound
    
    store_item_obj = await crud.get_store_item_by_id(
        db, store_item_id=store_item.id
    )
    if store_item_obj is None:
        raise StoreItemNotFound
    
    store_item_obj = await crud.update_store_item(
        db, store_item=store_item_obj, 
        **store_item.model_dump(exclude=["id", "sizes"]), sizes=sizes
    )
    return StoreItem.model_validate(store_item_obj)


async def delete_store_item(db: AsyncSession, store_item_id: int, 
                            current_user: User):
    await check_user_permission(current_user, transactions.DELETE_STORE_ITEM)
    
    store_item_obj = await crud.get_store_item_by_id(
        db, store_item_id=store_item_id
    )
    if store_item_obj is None:
        raise StoreItemNotFound
    
    await crud.delete_store_item(db, store_item=store_item_obj)
    
    
async def get_store_item(db: AsyncSession, store_item_id: int):
    store_item_obj = await crud.get_store_item_by_id(
        db, store_item_id=store_item_id   
    )
    if store_item_id is None:
        raise StoreItemNotFound
    
    return StoreItem.model_validate(store_item_obj)


async def get_all_categories(db: AsyncSession, limit: int, 
                             offset: int) -> list[str]:
    categories = await crud.get_all_store_categories(
        db, limit=limit, offset=offset
    )
    return [category.name for category in categories]