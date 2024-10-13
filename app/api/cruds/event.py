from datetime import datetime

from loguru import logger
from sqlalchemy import and_, extract, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Event


@logger.catch
async def create_event(db: AsyncSession, league: str, tour: str | None, 
                       start_date: datetime, end_date: datetime | None, 
                       location_id: int | None, first_team_id: int, 
                       second_team_id: int, first_team_score: int, 
                       second_team_score: int, stream_url: str) -> Event:
    """
    Creates an event in the database.

    Args:
        db (AsyncSession): SQLAlchemy AsyncSession object.
        league (str): League name.
        tour (str | None): Tour name.
        start_date (datetime): Event start date.
        end_date (datetime | None): Event end date.
        location_id (int | None): Event location id.
        first_team_id (int): First team id.
        second_team_id (int): Second team id.
        first_team_score (int): First team score.
        second_team_score (int): Second team score.
        stream_url (str): Event stream url.

    Returns:
        Event: Created event object.
    """
    event = Event(
        league=league, tour=tour, start_date=start_date.replace(tzinfo=None), 
        location_id=location_id, first_team_id=first_team_id, 
        second_team_id=second_team_id, 
        first_team_score=first_team_score, 
        second_team_score = second_team_score, stream_url=stream_url
    )
    
    if end_date:
        event.end_date = end_date.replace(tzinfo=None)    
    
    db.add(event)
    await db.commit()
    await db.refresh(event)
    
    return event


@logger.catch
async def get_all_events(db: AsyncSession, limit: int, 
                         offset: int, opponent_id: int | None,
                         year: int | None, month: int | None) -> list[Event]:
    query = (
        select(Event).order_by(Event.start_date).offset(offset).limit(limit)
    )
    
    print(year)
    
    if opponent_id:
        query = query.where(
            or_(
                Event.first_team_id == opponent_id,
                Event.second_team_id == opponent_id
            )
        )
    if year:
        query = query.where(
            extract("year", Event.start_date) == year
        )
    if month:
        query = query.where(
            extract("month", Event.start_date) == month
        )
        
    results = await db.execute(query)
    
    return results.scalars().all()


@logger.catch
async def get_current_event(db: AsyncSession) -> Event | None:
    """Gets the current event from the database.
    
    The current event is the event that does not have an end date and its start date
    is less than or equal to the current datetime.
    
    Args:
        db (AsyncSession): SQLAlchemy AsyncSession object.
    
    Returns:
        Event | None: The current event or None if no current event
    """
    results = await db.execute(
        select(Event).where(
            and_(
                Event.end_date == None,
                Event.start_date <= datetime.now()
            )
        )
    )
    return results.scalars().first()


@logger.catch
async def get_finished_events(db: AsyncSession, limit: int, 
                              offset: int) -> list[Event]:
    """Gets finished events from the database.
    
    Finished events are events that have an end date and that date is less than or
    equal to the current datetime.
    
    Args:
        db (AsyncSession): SQLAlchemy AsyncSession object.
        limit (int): Number of events to return.
        offset (int): Offset to start returning events from.
    
    Returns:
        list[Event]: List of finished events.
    """
    results = await db.execute(
        select(Event).where(
            and_(
                Event.end_date != None,
                Event.end_date <= datetime.now()
            )
        ).order_by(Event.start_date).offset(offset).limit(limit)
    )
    return results.scalars().all()


@logger.catch
async def get_future_events(db: AsyncSession, limit: int, 
                            offset: int) -> list[Event]:
    """Gets future events from the database.
    
    Future events are events that have a start date that is greater than the current
    datetime.
    
    Args:
        db (AsyncSession): SQLAlchemy AsyncSession object.
        limit (int): Number of events to return.
        offset (int): Offset to start returning events from.
    
    Returns:
        list[Event]: List of future events.
    """
    results = await db.execute(
        select(Event).where(
            and_(
                Event.start_date > datetime.now()
            )
        ).order_by(Event.start_date).offset(offset).limit(limit)
    )
    return results.scalars().all()


@logger.catch
async def get_event_by_id(db: AsyncSession, event_id: int) -> Event | None:
    """Gets an event from the database by its ID.
    
    Args:
        db (AsyncSession): SQLAlchemy AsyncSession object.
        event_id (int): ID of the event to get.
    
    Returns:
        Event | None: The event if found, otherwise None.
    """
    results = await db.execute(
        select(Event).where(Event.id == event_id)
    )
    return results.scalars().first()


@logger.catch
async def edit_event(db: AsyncSession, event: Event, league: str, tour: str,
                     start_date: datetime, end_date: datetime, 
                     location_id: int, first_team_id: int, second_team_id: int,
                     first_team_score: int, second_team_score: int) -> Event:
    """Edits an event in the database.
    
    Args:
        db (AsyncSession): SQLAlchemy AsyncSession object.
        event (Event): Event object to edit.
        league (str): League name.
        tour (str): Tour name.
        start_date (datetime): Event start date.
        end_date (datetime): Event end date.
        location_id (int): Event location id.
        first_team_id (int): First team id.
        second_team_id (int): Second team id.
        first_team_score (int): First team score.
        second_team_score (int): Second team score.
    
    Returns:
        Event: Edited event object.
    """
    event.league = league
    event.tour = tour
    event.start_date = start_date.replace(tzinfo=None)
    event.end_date = end_date.replace(tzinfo=None)
    event.location_id = location_id
    event.first_team_id = first_team_id
    event.second_team_id = second_team_id
    event.first_team_score = first_team_score
    event.second_team_score = second_team_score
    await db.commit()
    await db.refresh(event)
    return event


@logger.catch
async def delete_event(db: AsyncSession, event: Event):
    """Deletes an event from the database.
    
    Args:
        db (AsyncSession): SQLAlchemy AsyncSession object.
        event (Event): Event object to delete.
    """
    await db.delete(event)
    await db.commit()