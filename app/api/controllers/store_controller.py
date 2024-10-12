from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependecies.database import get_db
from ..schemas.store import StoreItem
from ..services import store_service

app = APIRouter()


@app.get("", response_model=list[StoreItem])
async def get_all_store_items(limit: int = 10, offset: int = 0, 
                              db: AsyncSession = Depends(get_db)):
    store_items = await store_service.get_all_store_items(
        db, limit=limit, offset=offset
    )
    return store_items