from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import transactions, db_constants

from ..cruds import news as crud
from ..dependecies.exceptions import NoPermissions
from ..schemas.news import News
from ..schemas.user import User
from ..services.user_service import check_user_permission

CATEGORY_NOT_FOUND = "Category not found"
NEWS_NOT_FOUND = "News not found"


async def get_news(db: AsyncSession, news_id: int) -> News:
    news = await crud.get_news_by_id(db, news_id=news_id)
    
    if news is None:
        raise HTTPException(
            status_code=404, detail=NEWS_NOT_FOUND
        )
    # if news.status == db_constants.NEWS_UNAVAILABLE and current_user is not None:
    #     if await check_user_permission()
    
    return News.model_validate(news)


async def get_all_news(db: AsyncSession, limit: int, offset: int, year: int | None, month: int | None) -> list[News]:
    news = await crud.get_all_news(db, limit=limit, offset=offset, year=year, month=month)
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
    return News.model_validate(news)
    

async def delete_news(db: AsyncSession, news_id: int, current_user: User):
    if not await check_user_permission(current_user, transactions.DELETE_NEWS):
        raise NoPermissions
    
    news = await crud.get_news_by_id(db, news_id=news_id)
    if news is None:
        raise HTTPException(
            status_code=404, detail=NEWS_NOT_FOUND
        )
    
    await crud.delete_news(db, user_id=current_user.id, news=news)
    

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
    
    news = await crud.update_news(db, user_id=current_user.id, news=old_news, **news.model_dump(exclude=["id"]))
    return news


async def get_all_categories(db: AsyncSession) -> list[str]:
    categories = await crud.get_all_news_categories(db)
    print([categorie.name for categorie in categories])
    return [categorie.name for categorie in categories]