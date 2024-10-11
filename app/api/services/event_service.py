from sqlalchemy.ext.asyncio import AsyncSession

from app.config import db_constants, transactions

from .. import models
from ..cruds import event as crud
from ..cruds import location as l_crud
from ..cruds import settings as s_crud
from ..cruds import team as t_crud
from ..dependecies.exceptions import (LocationNotFound, NoPermissions,
                                      TeamNotFound, EventNotFound)
from ..schemas.event import CreateEvent, Event, EditEvent
from ..schemas.team import Team
from ..schemas.user import User
from ..services.user_service import check_user_permission


async def create_event(db: AsyncSession, event: CreateEvent, 
                       current_user: User) -> Event:
    if not await check_user_permission(
        current_user, transactions.CREATE_EVENT
    ):
        raise NoPermissions
    
    first_team_id = None
    second_team_id = None
    
    if event.first_team_id is not None:
        team_obj = await t_crud.get_team_by_id(
            db, team_id=event.second_team_id
        )
        if team_obj is None:
            raise TeamNotFound
        
        first_team_id = event.first_team_id
    
    if event.second_team_id is not None:
        team_obj = await t_crud.get_team_by_id(
            db, team_id=event.second_team_id
        )
        if team_obj is None:
            raise TeamNotFound
        
        second_team_id = event.second_team_id
    
    if event.location_id != None:
        location = await l_crud.get_location_by_id(db, event.location_id)
        if location is None:
            raise LocationNotFound
    
    if first_team_id is None:
        first_team_id = await s_crud.get_settings(
            db, name=db_constants.BASE_TEAM
        )
        first_team_id = int(first_team_id.value)
        event = await crud.create_event(
            db, **event.model_dump(exclude=["first_team_id"]), 
            first_team_id=first_team_id
        )
    else:
        second_team_id = await s_crud.get_settings(
            db, name=db_constants.BASE_TEAM
        )
        second_team_id = int(second_team_id.value)
        event = await crud.create_event(
            db, **event.model_dump(exclude=["second_team_id"]), 
            second_team_id=second_team_id
        )
    
    return await validate_event_model(event)


async def get_all_events(db: AsyncSession, limit: int,
                         offset: int, page: str) -> list[Event]:
    if page == "main":
        current_event = await crud.get_current_event(db)
        
        future_limit = 2 if current_event else 1
        future_events = await crud.get_future_events(
            db, limit=future_limit, offset=0
        )
        
        finished_limit = (2 - len(future_events) + future_limit) \
            if future_events else 2 + future_limit
        
        finished_events = await crud.get_finished_events(
            db, limit=finished_limit, offset=0
        )
        
        events = []
        if current_event is not None:
            events.append(await validate_event_model(current_event))
        
        events.extend(
            [await validate_event_model(event) for event in future_events]
        )
        events.extend(
            [await validate_event_model(event) for event in finished_events]
        )

    else:
        events_objs = await crud.get_all_events(
            db, limit=limit, offset=offset
        )
        events = [await validate_event_model(event) for event in events_objs]
    return events


async def edit_event(db: AsyncSession, event: EditEvent, 
                     current_user: User) -> Event:
    if not await check_user_permission(current_user, transactions.EDIT_EVENT):
        raise NoPermissions
    
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
    
    event_obj = await crud.edit_event(
        db, event=event_obj, **event.model_dump(exclude=["id"])
    )
    event = await validate_event_model(event_obj)
    
    return event


async def validate_event_model(event: models.Event) -> Event:
    first_team = Team.model_validate(event.first_team)
    first_team.score = event.first_team_score
    second_team = Team.model_validate(event.second_team)
    second_team.score = event.second_team_score
    
    validated_event = Event(
        id=event.id, league=event.league, tour=event.tour, 
        start_date=event.start_date, end_date=event.end_date, 
        first_team=first_team, second_team=second_team,
        location_name=event.location.name if event.location else None,
        location_address=event.location.address if event.location else None
    )
    
    return validated_event