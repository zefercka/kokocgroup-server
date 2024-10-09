from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

from app.config import team_member_settings

from ..schemas.user import User

from datetime import date


class Team(BaseModel):
    trainers: list["Member"]
    goalkeepers: list["Member"]
    defenders: list["Member"]
    midfielders: list["Member"]
    strikers: list["Member"]
    admins: list["Member"]
    

class Member(BaseModel):
    position: str
    height: Optional[int]
    weight: Optional[int]
    user_id: int
    first_name: str = ""
    last_name: str = ""
    date_of_birth: date = ""
    avatar_url: Optional[str] = ""
    
    class Config:
        from_attributes = True
