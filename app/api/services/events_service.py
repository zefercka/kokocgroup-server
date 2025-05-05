from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.cruds import event as crud
from app.api.cruds import location as l_crud
from app.api.cruds import team as t_crud
from app.api.dependencies.enums import EventPages
from app.api.dependencies.exceptions import (EventNotFound,
                                             InternalServerError,
                                             InvalidPageType, LocationNotFound,
                                             TeamNotFound)
from app.api.dependencies.validators import validate_event_model
from app.api.schemas.event import CreateEvent, EditEvent, Event
from app.api.schemas.user import User
from app.api.services import locations_service, teams_service
from app.api.services.users_service import check_user_permission
from app.config import transactions
from app.logger import logger


async def create_event(
    db: AsyncSession,
    event: CreateEvent,
    current_user: User
) -> Event:
    await check_user_permission(current_user, transactions.CREATE_EVENT)

    # Если команды нет, то вызовет исключение
    await teams_service.get_team(db, team_id=event.first_team_id)
    # Если команды нет, то вызовет исключение
    await teams_service.get_team(db, team_id=event.second_team_id)
    
    if event.location_id:
        # Если локации нет, то вызовет исключение
        await locations_service.get_location(db, event.location_id)
    
    try:
        created_event = await crud.create_event(db, **event.model_dump())
        return validate_event_model(created_event)
    
    except Exception as err:
        logger.error(err, exc_info=True)
        raise InternalServerError


async def get_all_events(
    db: AsyncSession,
    limit: int,
    offset: int,
    page: str,
    opponent_id: Optional[int], 
    year: Optional[int],
    month: Optional[int]
) -> list[Event]:
    try:
        events: list[Event] = []
        
        if page == EventPages.MAIN:
            current_event = await crud.get_current_event(db)
            
            future_limit = 1 if current_event else 2
            future_events = await crud.get_future_events(
                db, limit=future_limit, offset=0
            )
            
            finished_limit = (2 - len(future_events) + future_limit) \
                if future_events else 2 + future_limit
            
            finished_events = await crud.get_finished_events(
                db, limit=finished_limit, offset=0
            )
            
            if current_event:
                events.append(validate_event_model(current_event))

            for event_group in [future_events, finished_events]:
                if event_group:
                    events.extend([validate_event_model(e) for e in event_group])

        elif page == EventPages.EVENT:
            events_objs = await crud.get_all_events(
                db, limit=limit, offset=offset, opponent_id=opponent_id,
                year=year, month=month
            )
            
            events = [validate_event_model(event) for event in events_objs]
                    
        else:
            raise InvalidPageType
            
        return events
    except HTTPException:
        raise
    except Exception as err:
        logger.error(err, exc_info=True)
        raise InternalServerError
        


async def edit_event(
    db: AsyncSession,
    event: EditEvent,
    current_user: User
) -> Event:
    await check_user_permission(current_user, transactions.EDIT_EVENT)
    
    event_obj = await crud.get_event_by_id(db, event_id=event.id)
    if event_obj is None:
        raise EventNotFound
    
    if event_obj.first_team_id != event.first_team_id:
        first_team_obj = await t_crud.get_team_by_id(
            db, team_id=event.first_team_id
        )
        if first_team_obj is None:
            raise TeamNotFound
    
    if event_obj.second_team_id != event.second_team_id:
        second_team_obj = await t_crud.get_team_by_id(
            db, team_id=event.second_team_id
        )
        if second_team_obj is None:
            raise TeamNotFound
    
    if event_obj.location_id != event.location_id:
        location_obj = await l_crud.get_location_by_id(
            db, location_id=event.location_id
        )
        if location_obj is None:
            raise LocationNotFound
    
    try:
        event_obj = await crud.edit_event(
            db, event=event_obj,
            **event.model_dump(exclude_unset=True, exclude=["id"])
        )
        event = validate_event_model(event_obj)
        
        return event
    except Exception as err:
        logger.error(err, exc_info=True)
        raise InternalServerError


async def delete_event(
    db: AsyncSession,
    event_id: int,
    current_user: User
) -> None:
    await check_user_permission(current_user, transactions.DELETE_EVENT)
    
    event_obj = await crud.get_event_by_id(db, event_id=event_id)
    if event_obj is None:
        raise EventNotFound
    
    try:
        await crud.delete_event(db, event=event_obj)
        logger.info(f"Event {event_id} deleted by user {current_user.id}")
    except Exception as err:
        logger.error(err, exc_info=True)
        raise InternalServerError
    

async def get_event_by_id(
    db: AsyncSession,
    event_id: int
) -> Event:
    event_obj = await crud.get_event_by_id(db, event_id=event_id)
    if event_obj is None:
        raise EventNotFound
    
    return validate_event_model(event_obj)