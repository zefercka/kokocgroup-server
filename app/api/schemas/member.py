from datetime import date
from typing import Optional

from pydantic import BaseModel

from ..dependecies.enums import MemberRoles, MemberStatuses


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
    status: MemberStatuses
    

class EditMember(BaseMember):
    id: int
    role: MemberRoles
    status: MemberStatuses