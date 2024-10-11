from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.config import team_member_settings


class MemberRoles(Enum):
    player = team_member_settings.PLAYER_ROLE
    trainer= team_member_settings.TRAINER_ROLE
    admin = team_member_settings.ADMIN_ROLE
    

class MemberStatus(Enum):
    present = team_member_settings.PRESENT_STATUS
    past = team_member_settings.PAST_STATUS


class TeamList(BaseModel):
    trainers: list["Member"]
    goalkeepers: list["Member"]
    defenders: list["Member"]
    midfielders: list["Member"]
    strikers: list["Member"]
    admins: list["Member"]
    

class BaseMember(BaseModel):
    position: str
    height: Optional[int] = None
    weight: Optional[int] = None
    user_id: int
    
    class Config:
        from_attributes = True


class Member(BaseMember):
    id: int
    first_name: str = ""
    last_name: str = ""
    date_of_birth: date = ""
    avatar_url: Optional[str] = ""


class NewMember(BaseMember):
    role: MemberRoles
    status: MemberStatus
    

class EditMember(BaseMember):
    id: int
    role: MemberRoles
    status: MemberStatus