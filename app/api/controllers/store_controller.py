from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db
from app.api.dependencies.enums import StoreItemFilters
from app.api.schemas.store import CreateStoreItem, StoreItem
from app.api.schemas.user import User
from app.api.services import store_service
from app.api.services.auth_service import get_current_user

app = APIRouter()


@app.get("/categories", response_model=list[str])
async def get_store_categories(limit: int = 20, offset: int = 0, 
                               db: AsyncSession = Depends(get_db)):
    categories = await store_service.get_all_categories(
        db, limit=limit, offset=offset
    )
    return categories


@app.get("", response_model=list[StoreItem])
async def get_all_store_items(limit: int = 10, offset: int = 0, 
                              category: str | None = None,
                              filter: StoreItemFilters = StoreItemFilters.NEW,
                              db: AsyncSession = Depends(get_db)):
    store_items = await store_service.get_all_store_items(
        db, limit=limit, offset=offset, category=category, filter=filter
    )
    return store_items


@app.get("/{store_item_id}", response_model=StoreItem)
async def get_store_item(store_item_id: int, 
                         db: AsyncSession = Depends(get_db)):
    store_item = await store_service.get_store_item(
        db, store_item_id=store_item_id
    )
    return store_item


@app.post("", response_model=StoreItem)
async def create_store_item(store_item: CreateStoreItem,
                            current_user: User = Depends(get_current_user),
                            db: AsyncSession = Depends(get_db)):
    store_item = await store_service.create_store_item(
        db, store_item=store_item, current_user=current_user
    )
    return store_item


@app.put("", response_model=StoreItem)
async def edit_store_item(store_item: StoreItem, 
                          current_user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    store_item = await store_service.edit_store_item(
        db, store_item=store_item, current_user=current_user   
    )
    return store_item


@app.delete("/{store_item_id}")
async def delete_store_item(store_item_id: int, 
                            current_user: User = Depends(get_current_user),
                            db: AsyncSession = Depends(get_db)):
    await store_service.delete_store_item(
        db, store_item_id=store_item_id, current_user=current_user
    )