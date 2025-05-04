from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db
from app.api.dependencies.enums import EventPages
from app.api.schemas.event import CreateEvent, EditEvent, Event
from app.api.schemas.user import User
from app.api.services import events_service
from app.api.services.auth_service import get_current_user

app = APIRouter()


@app.post("", response_model=Event)
async def create_event(event: CreateEvent, 
                       current_user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    return await events_service.create_event(
        db, event=event, current_user=current_user
    )
    

@app.get("", response_model=list[Event])
async def get_all_events(limit: int = 10, offset: int = 0, 
                         page: EventPages = EventPages.MAIN,
                         opponent_id: int | None = None,
                         year: int | None = None,
                         month: int | None = None,
                         db: AsyncSession = Depends(get_db)):
    events = await events_service.get_all_events(
        db, limit=limit, offset=offset, page=page, opponent_id=opponent_id,
        year=year, month=month
    )
    return events


@app.get("/{event_id}", response_model=Event)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    return await events_service.get_event_by_id(db, event_id=event_id)


@app.put("", response_model=Event)
async def edit_event(event: EditEvent, 
                     current_user: User = Depends(get_current_user),
                     db: AsyncSession = Depends(get_db)):
    return await events_service.edit_event(
        db, event=event, current_user=current_user
    )
    

@app.delete("/{event_id}", response_model=Event)
async def delete_event(event_id: int, 
                       current_user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    return await events_service.delete_event(
        db, event_id=event_id, current_user=current_user
    )