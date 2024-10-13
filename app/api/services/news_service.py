from sqlalchemy.ext.asyncio import AsyncSession

from app.config import db_constants, transactions

from ..cruds import news as crud
from ..dependecies.exceptions import CategoryNotFound, NewsNotFound
from ..schemas.news import News
from ..schemas.user import User
from .users_service import check_user_permission


async def get_news(db: AsyncSession, news_id: int) -> News:
    news = await crud.get_news_by_id(db, news_id=news_id)
    
    if news is None or news.status == db_constants.NEWS_UNAVAILABLE:
        raise NewsNotFound
    
    return News.model_validate(news)


async def get_all_news(db: AsyncSession, limit: int, offset: int, 
                       year: int | None, month: int | None, search: str | None,
                       category: str | None) -> list[News]:
    news = await crud.get_all_news(
        db, limit=limit, offset=offset, year=year, month=month, 
        category=category, search=search
    )
    news = [News.model_validate(news_) for news_ in news]
    return news


async def get_all_deleted_news(db: AsyncSession,  limit: int, offset: int, 
                               year: int | None, month: int | None,
                               category: str | None,
                               current_user: User) -> list[News]:
    await check_user_permission(current_user, transactions.VIEW_DELETED_NEWS)
    
    news = await crud.get_all_deleted_news(
        db, limit=limit, offset=offset, year=year, month=month,
        category=category
    )
    news = [News.model_validate(news_) for news_ in news]
    return news


async def create_news(db: AsyncSession, news: News, current_user: User) -> News:    
    await check_user_permission(current_user, transactions.CREATE_NEWS)

    category = await crud.get_news_category(db, news.category_name)
    if category is None:
        raise CategoryNotFound
    
    news = await crud.add_news(
        db, user_id=current_user.id, **news.model_dump(exclude=["id"])
    )
    return News.model_validate(news)
    

async def delete_news(db: AsyncSession, news_id: int, current_user: User):
    check_user_permission(current_user, transactions.DELETE_NEWS)
    
    news = await crud.get_news_by_id(db, news_id=news_id)
    if news is None:
        raise NewsNotFound
    
    await crud.delete_news(db, user_id=current_user.id, news=news)
    

async def update_news(db: AsyncSession, news: News, current_user: User) -> News:
    await check_user_permission(current_user, transactions.EDIT_NEWS)
    
    old_news = await crud.get_news_by_id(db, news_id=news.id)
    if old_news is None:
        raise NewsNotFound
    
    category = await crud.get_news_category(db, news.category_name)
    if category is None:
        raise CategoryNotFound
    
    news = await crud.update_news(
        db, user_id=current_user.id, news=old_news, 
        **news.model_dump(exclude=["id"])
    )
    return news.model_validate(news)


async def get_all_categories(db: AsyncSession) -> list[str]:
    categories = await crud.get_all_news_categories(db)
    return [categorie.name for categorie in categories]


async def get_deleted_news(db: AsyncSession, news_id: int, 
                           current_user: User) -> News:
    await check_user_permission(current_user, transactions.VIEW_DELETED_NEWS)
    
    news = await crud.get_news_by_id(db, news_id=news_id)
    if news is None or news.status != db_constants.NEWS_UNAVAILABLE:
        raise NewsNotFound
    
    return News.model_validate(news)


async def get_all_scheduled_news(db: AsyncSession, limit: int, offset: int, 
                                 year: int | None, month: int | None,
                                 category: str | None,
                                 current_user: User) -> list[News]:
    await check_user_permission(current_user, transactions.VIEW_SHEDULED_NEWS)
    
    news = await crud.get_all_scheduled_news(
        db, limit=limit, offset=offset, year=year, month=month, 
        category=category
    )
    news = [News.model_validate(news_) for news_ in news]
    return news