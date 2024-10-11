from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator

from ..schemas.team import EventTeam


class EventBase(BaseModel):
    league: str
    tour: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    
    class Config:
        from_attributes=True
    

class CreateEvent(EventBase):
    location_id: Optional[int] = None
    first_team_id: Optional[int] = None
    second_team_id: Optional[int] = None
    first_team_score: Optional[int] = 0
    second_team_score: Optional[int] = 0
    
    @model_validator(mode="after")
    def at_least_one_team_id(cls, values):
        if values.first_team_id == values.second_team_id:
            raise ValueError("First and second team must be different")
        return values


class Event(EventBase):
    id: int
    first_team: EventTeam
    second_team: EventTeam
    location_name: Optional[str]
    location_address: Optional[str]
    
    
class EditEvent(CreateEvent):
    id: int