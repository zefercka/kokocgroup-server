from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from datetime import datetime
from ..schemas import News, User
from ..cruds.news import get_news_by_id, add_news
from ..cruds.permission import get_permission
from app.config import transactions
from ..services.user_service import check_user_permission
from ..dependecies.exceptions import NoPermissions


async def get_news_by_id(db: AsyncSession, news_id: int):
    news = await get_news_by_id(db, news_id=news_id)
    return news


async def create_news(db: AsyncSession, news: News, current_user: User) -> News:    
    if await check_user_permission(db, current_user, transactions.CREATE_NEWS):
        news = await add_news(db, user_id=current_user.id, **news.model_dump(exclude=["id"]))
        return news
    
    raise NoPermissions
    