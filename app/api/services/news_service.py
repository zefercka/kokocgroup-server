from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from datetime import datetime
from ..schemas.news import News
from ..schemas.user import User
from ..cruds import news as crud
from app.config import transactions
from ..services.user_service import check_user_permission
from ..dependecies.exceptions import NoPermissions


CATEGORY_NOT_FOUND = "Category not found"
NEWS_NOT_FOUND = "News not found"


async def get_news(db: AsyncSession, news_id: int) -> News:
    news = await crud.get_news_by_id(db, news_id=news_id)
    return news


async def get_all_news(db: AsyncSession, limit: int, offset: int) -> list[News]:
    news = await crud.get_all_news(db, limit=limit, offset=offset)
    return news


async def create_news(db: AsyncSession, news: News, current_user: User) -> News:    
    if not await check_user_permission(current_user, transactions.CREATE_NEWS):
        raise NoPermissions

    category = await crud.get_news_category(db, news.category_name)
    if category is None:
        raise HTTPException(
            status_code=404, detail=CATEGORY_NOT_FOUND
        )
    
    news = await crud.add_news(db, user_id=current_user.id, **news.model_dump(exclude=["id"]))
    return news
    

async def delete_news(db: AsyncSession, news_id: int, current_user: User):
    if not await check_user_permission(current_user, transactions.DELETE_NEWS):
        return NoPermissions
    
    news = await crud.get_news_by_id(db, news_id=news_id)
    if news is None:
        raise HTTPException(
            status_code=404, detail=NEWS_NOT_FOUND
        )
    
    await crud.delete_news(db, news=news)
    

async def update_news(db: AsyncSession, news: News, current_user: User) -> News:
    if not await check_user_permission(current_user, transactions.EDIT_NEWS):
        return NoPermissions
    
    old_news = await crud.get_news_by_id(db, news_id=news.id)
    if old_news is None:
        raise HTTPException(
            status_code=404, detail=NEWS_NOT_FOUND
        )
    
    category = await crud.get_news_category(db, news.category_name)
    if category is None:
        raise HTTPException(
            status_code=404, detail=CATEGORY_NOT_FOUND
        )
    
    news = await crud.update_news(db, news=old_news, **news.model_dump(exclude=["id"]))
    return news


async def get_all_categories(db: AsyncSession) -> list[str]:
    categories = await crud.get_all_news_categories(db)
    print([categorie.name for categorie in categories])
    return [categorie.name for categorie in categories]