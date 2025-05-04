from datetime import datetime, timedelta

from loguru import logger
from sqlalchemy import and_, delete, extract, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models import News, NewsAction, NewsCategory
from app.config import db_constants


@logger.catch
async def get_news_by_id(db: AsyncSession, news_id: int) -> News | None:
    """
    Get a news item from the database by its ID.

    Args:
        db (AsyncSession): The database session.
        news_id (int): The ID of the news item to get.

    Returns:
        News | None: The news item if found, otherwise None.
    """
    results = await db.execute(select(News).where(News.id == news_id))
    return results.scalars().first()


@logger.catch
async def get_all_news(db: AsyncSession, limit: int, offset: int, 
                       year: int | None, month: int | None,
                       category: str | None, search: str | None) -> list[News]:
    """
    Get all available news from the database, 
    filtered by given year and month if provided.

    Args:
        db (AsyncSession): The database session.
        limit (int): The number of news to return.
        offset (int): The offset from the start of the result set.
        year (int | None): The year to filter by, if provided.
        month (int | None): The month to filter by, if provided.

    Returns:
        list[News]: The list of news.
    """
    query = (
        select(News)
        .where(
            and_(
                # Only include news items that have a date in the past
                News.news_date <= datetime.now(), 
                # Only include news items that are available
                News.status == db_constants.NEWS_AVAILABLE
            )
        )
        # Order by news_date in descending order and id in ascending order
        .order_by(News.news_date.desc(), News.id.asc())
        # Skip the first offset items
        .offset(offset)
        # Limit the result set to limit
        .limit(limit)
    )

    if year is not None:
        # Filter by year if provided
        query = query.where(extract("year", News.news_date) == year)
    if month is not None:
        # Filter by month if provided
        query = query.where(extract("month", News.news_date) == month)
    if category is not None:
        # Filter by category if provided
        query = query.where(News.category_name == category)
    if search is not None:
        query = query.where(
            or_(
                News.title.icontains(search),
                News.content.icontains(search),
                func.to_tsvector(
                    func.coalesce(News.title, '') + ' ' +
                    func.coalesce(News.content, ''))
                .op('@@')(func.to_tsquery(' & '.join(search.split())))
            )
        )

    results = await db.execute(query)
    return results.scalars().all()


@logger.catch
async def get_all_deleted_news(db: AsyncSession, limit: int, offset: int, 
                               year: int | None = None, 
                               month: int | None = None,
                               category: str | None = None) -> list[News]:
    """
    Get all deleted news from the database, 
    filtered by given year and month if provided.

    Args:
        db (AsyncSession): The database session.
        limit (int): The maximum number of news items to return.
        offset (int): The number of news items to skip before returning.
        year (int | None): The year to filter the news items by.
        month (int | None): The month to filter the news items by.

    Returns:
        list[News]: A list of deleted news items.
    """
    query = (
        select(News)
        .where(
            # Only include news items that are no longer available
            News.status == db_constants.NEWS_UNAVAILABLE
        )
        .order_by(News.news_date.desc(), News.id.asc())
        .offset(offset)
        .limit(limit)
    )
    if year is not None:
        # Filter by year if provided
        query = query.where(extract("year", News.news_date) == year)
    if month is not None:
        # Filter by month if provided
        query = query.where(extract("month", News.news_date) == month)
    if category is not None:
        # Filter by category if provided
        query = query.where(News.category_name == category)
        
    results = await db.execute(query)
    return results.scalars().all()


@logger.catch
async def get_news_category(db: AsyncSession, name: str) -> NewsCategory | None:
    """
    Get a news category by name from the database.

    Args:
        db (AsyncSession): The database session.
        name (str): The name of the news category.

    Returns:
        NewsCategory | None: The news category if found, or None.
    """
    results = await db.execute(select(NewsCategory).where(NewsCategory.name == name))
    return results.scalars().first()


@logger.catch
async def add_news_action(db: AsyncSession, user_id: int, news_id: int, 
                          action_type: str) -> NewsAction:
    """
    Add a new news action to the database.

    Args:
        db (AsyncSession): The database session.
        user_id (int): The ID of the user performing the action.
        news_id (int): The ID of the news item being acted on.
        action_type (str): The type of action being performed.

    Returns:
        NewsAction: The newly created news action.
    """
    news_action = NewsAction(
        user_id=user_id, news_id=news_id, type=action_type
    )
    db.add(news_action)
    await db.commit()
    await db.refresh(news_action)
    return news_action


@logger.catch
async def add_news(db: AsyncSession, user_id: int, title: str, 
                   news_date: datetime, content: str, category_name: str,
                   image_url: str) -> News:
    """
    Add a new news item to the database.

    Args:
        db (AsyncSession): The database session.
        user_id (int): The ID of the user creating the news item.
        title (str): The title of the news item.
        news_date (datetime): The date the news item was published.
        content (str): The content of the news item.
        category_name (str): The name of the news category.
        image_url (str): The URL of the news item's image.

    Returns:
        News: The newly created news item.
    """
    news = News(
        title=title, news_date=news_date.replace(tzinfo=None), content=content,
        category_name=category_name, image_url=image_url
    )

    db.add(news)
    await db.commit()
    await db.refresh(news)
    
    await add_news_action(
        db, user_id=user_id, news_id=news.id, action_type="create"
    )
    
    return news


@logger.catch
async def delete_news(db: AsyncSession, user_id: int, news: News):
    if news.status == db_constants.NEWS_AVAILABLE:
        news.status = db_constants.NEWS_UNAVAILABLE
        await db.commit()
        await add_news_action(
            db, user_id=user_id, news_id=news.id, action_type="delete"
        )
    elif news.status == db_constants.NEWS_UNAVAILABLE:
        await db.delete(news)
        await db.commit()

        
@logger.catch    
async def update_news(db: AsyncSession, user_id, news: News, title: str, 
                      news_date: str, content: str, category_name: str, 
                      image_url: str) -> News | None:    
    news.title = title
    news.news_date = news_date.replace(tzinfo=None)
    news.content = content
    news.category_name = category_name
    news.image_url = image_url
    await db.commit()
    await db.refresh(news)
    
    await add_news_action(
        db, user_id=user_id, news_id=news.id, action_type="edit"
    )
    
    return news
    
   
@logger.catch 
async def get_all_news_categories(db: AsyncSession) -> list[NewsCategory]:
    results = await db.execute(select(NewsCategory))
    return results.scalars().all()


@logger.catch
async def get_all_scheduled_news(db: AsyncSession, 
                                 limit: int, offset: int, year: int | None, 
                                 month: int | None) -> list[News]:
    query = (
        select(News)
        .where(
            and_(
                News.news_date > datetime.now(),
                News.status == db_constants.NEWS_AVAILABLE
            )
        ).order_by(
            News.news_date.desc(),
            News.id.asc()
        )
        .offset(offset)
        .limit(limit)
    )
    
    if year is not None:
        # Filter by year if provided
        query = query.where(extract("year", News.news_date) == year)
    if month is not None:
        # Filter by month if provided
        query = query.where(extract("month", News.news_date) == month)
        
    results = await db.execute(query)
    return results.scalars().all()


@logger.catch
async def delete_expired_news(db: AsyncSession):
    results = await db.execute(
        select(NewsAction.news_id).where(
            and_(
                NewsAction.type == "delete",
                NewsAction.created_at.op('+')(
                    timedelta(days=db_constants.DELETE_NEWS_AFTER)) 
                < datetime.now()
            )
        )
    )
    news_ids = results.scalars().all()
    
    await db.execute(
        delete(News).where(
            and_(
                News.status == db_constants.NEWS_UNAVAILABLE,   
                News.id.in_(news_ids)        
            )
        )
    )