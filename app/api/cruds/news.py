from datetime import datetime

from sqlalchemy import extract, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import db_constants

from ..models import News, NewsAction, NewsCategory

from app.config import db_constants


async def get_news_by_id(db: AsyncSession, news_id: int):
    results = await db.execute(select(News).where(News.id == news_id))
    return results.scalars().first()


async def get_all_news(db: AsyncSession, limit: int, offset: int, year: int | None, month: int | None):
    query = select(News).where(
        and_(
            News.news_date<=datetime.now(), 
            News.status == db_constants.NEWS_AVAILABLE
        )
    ).order_by(News.news_date.desc()).offset(offset).limit(limit)
    if year is not None:
        query = query.where(extract("year", News.news_date) == year)
    if month is not None:
        query = query.where(extract("month", News.news_date) == month)
    results = await db.execute(query)
    return results.scalars().all()


async def get_news_category(db: AsyncSession, name: str):
    results = await db.execute(select(NewsCategory).where(NewsCategory.name == name))
    return results.scalars().first()


async def add_news_action(db: AsyncSession, user_id: int, news_id: int, action_type: str):
    news_action = NewsAction(user_id=user_id, news_id=news_id, type=action_type)
    db.add(news_action)
    await db.commit()
    await db.refresh(news_action)
    return news_action


async def add_news(db: AsyncSession, user_id: int, title: str, news_date: datetime, content: str, category_name: str,
                   image_url: str):
    news = News(
        title=title, news_date=news_date.replace(tzinfo=None), content=content, category_name=category_name, image_url=image_url
    )

    db.add(news)
    await db.commit()
    await db.refresh(news)
    
    await add_news_action(db, user_id=user_id, news_id=news.id, action_type="create")
    
    return news


async def delete_news(db: AsyncSession, user_id: int, news: News):
    if news.status == db_constants.NEWS_AVAILABLE:
        news.status = db_constants.NEWS_UNAVAILABLE
        await db.commit()
        await add_news_action(db, user_id=user_id, news_id=news.id, action_type="delete")
    elif news.status == db_constants.NEWS_UNAVAILABLE:
        await db.delete(news)
        await db.commit()

        
    
async def update_news(db: AsyncSession, user_id, news: News, title: str, news_date: str, content: str, 
                      category_name: str, image_url: str) -> News | None:    
    news.title = title
    news.news_date = news_date.replace(tzinfo=None)
    news.content = content
    news.category_name = category_name
    news.image_url = image_url
    await db.commit()
    await db.refresh(news)
    
    await add_news_action(db, user_id=user_id, news_id=news.id, action_type="edit")
    
    return news
    
    
async def get_all_news_categories(db: AsyncSession) -> list[NewsCategory]:
    results = await db.execute(select(NewsCategory))
    print(results.scalars().all())
    return results.scalars().all()