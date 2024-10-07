from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from datetime import datetime
from ..schemas.news import News
from ..schemas.user import User
from ..cruds import news as crud
from app.config import transactions
from ..services.user_service import check_user_permission
from ..dependecies.exceptions import NoPermissions


async def get_news(db: AsyncSession, news_id: int) -> News:
    news = await crud.get_news_by_id(db, news_id=news_id)
    return news


async def get_all_news(db: AsyncSession, limit: int, offset: int) -> list[News]:
    news = await crud.get_all_news(db, limit=limit, offset=offset)


async def create_news(db: AsyncSession, news: News, current_user: User) -> News:    
    if await check_user_permission(db, current_user, transactions.CREATE_NEWS):
        news = await crud.add_news(db, user_id=current_user.id, **news.model_dump(exclude=["id"]))
        return news
    
    raise NoPermissions
    