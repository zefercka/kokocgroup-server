from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import team_member_settings

from ..models import Event

from datetime import datetime


async def create_event(db: AsyncSession, league: str, tour: str | None, 
                       start_date: datetime, end_date: datetime | None, 
                       location_id: int | None, first_team_id: int, 
                       second_team_id: int, first_team_score: int, 
                       second_team_score: int) -> Event:
    event = Event(
        league=league, tour=tour, start_date=start_date.replace(tzinfo=None), 
        end_date=end_date.replace(tzinfo=None),location_id=location_id, 
        first_team_id=first_team_id, second_team_id=second_team_id, 
        first_team_score=first_team_score, 
        second_team_score = second_team_score
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    
    return event


async def get_all_events(db: AsyncSession, limit: int, 
                         offset: int) -> list[Event]:
    results = await db.execute(
        select(Event).order_by(Event.start_date).offset(offset).limit(limit)
    )
    return results.scalars().all()


async def get_current_event(db: AsyncSession) -> Event:
    results = await db.execute(
        select(Event).where(
            and_(
                Event.end_date == None,
                Event.start_date <= datetime.now()
            )
        )
    )
    return results.scalars().first()


async def get_finished_events(db: AsyncSession, limit: int, 
                              offset: int) -> list[Event]:
    results = await db.execute(
        select(Event).where(
            and_(
                Event.end_date != None,
                Event.end_date <= datetime.now()
            )
        ).order_by(Event.start_date).offset(offset).limit(limit)
    )
    return results.scalars().all()


async def get_future_events(db: AsyncSession, limit: int, 
                            offset: int) -> list[Event]:
    results = await db.execute(
        select(Event).where(
            and_(
                Event.start_date > datetime.now()
            )
        ).order_by(Event.start_date).offset(offset).limit(limit)
    )
    return results.scalars().all()


async def get_event_by_id(db: AsyncSession, event_id: int):
    results = await db.execute(
        select(Event).where(Event.id == event_id)
    )
    return results.scalars().first()


async def edit_event(db: AsyncSession, event: Event, league: str, tour: str,
                     start_date: datetime, end_date: datetime, 
                     location_id: int, first_team_id: int, second_team_id: int,
                     first_team_score: int, second_team_score: int) -> Event:
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
