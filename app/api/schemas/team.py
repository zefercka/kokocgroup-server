from typing import Optional

from pydantic import BaseModel


class BaseTeam(BaseModel):
    name: str
    logo_url: str

    class Config:
        from_attributes = True


class EventTeam(BaseTeam):
    id: int
    name: str
    logo_url: str
    score: Optional[int] = 0
    

class Team(BaseTeam):
    id: int
        
        
class CreateTeam(BaseTeam):
    pass