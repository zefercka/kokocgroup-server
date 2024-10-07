from ..models import News, NewsAction
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime


async def get_news_by_id(db: AsyncSession, news_id: int):
    results = await db.execute(select(News).where(News.id == news_id))
    return results.scalars().first()


async def add_news_action(db: AsyncSession, user_id: int, news_id: int, action_type: str):
    news_action = NewsAction(user_id=user_id, news_id=news_id, type=action_type)
    db.add(news_action)
    await db.commit()
    await db.refresh(news_action)
    return news_action


async def add_news(db: AsyncSession, user_id: int, title: str, news_date: datetime, content: str, category: str,
                   image_url: str = "default"):
    news = News(
        title=title, news_date=news_date.replace(tzinfo=None), content=content, category=category, image_url=image_url
    )

    db.add(news)
    await db.commit()
    await db.refresh(news)
    
    await add_news_action(db, user_id=user_id, news_id=news.id, action_type="create")
    
    return news