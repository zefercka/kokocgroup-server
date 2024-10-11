from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependecies.database import get_db
from ..schemas.event import Event, CreateEvent, EditEvent
from ..schemas.user import User
from ..services.auth_service import get_current_user
from ..services import event_service

app = APIRouter()


@app.post("", response_model=Event)
async def create_event(event: CreateEvent, 
                       current_user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    return await event_service.create_event(
        db, event=event, current_user=current_user
    )
    

@app.get("", response_model=list[Event])
async def get_all_events(limit: int = 10, offset: int = 0, page: str = "main",
                         db: AsyncSession = Depends(get_db)):
    events = await event_service.get_all_events(
        db, limit=limit, offset=offset, page=page
    )
    return events


@app.put("", response_model=Event)
async def edit_event(event: EditEvent, 
                     current_user: User = Depends(get_current_user),
                     db: AsyncSession = Depends(get_db)):
    return await event_service.edit_event(
        db, event=event, current_user=current_user
    )