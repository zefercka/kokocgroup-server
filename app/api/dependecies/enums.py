from enum import Enum
from app.config import team_member_settings


class StoreItemFilters(Enum):
    NEW = "new"
    EXPENSIVE = "expensive"
    CHEAP = "cheap"
    

class MemberStatuses(Enum):
    PRESENT = team_member_settings.PRESENT_STATUS
    PAST = team_member_settings.PAST_STATUS
    

class MemberRoles(Enum):
    PLAYER = team_member_settings.PLAYER_ROLE
    TRAINER= team_member_settings.TRAINER_ROLE
    ADMIN = team_member_settings.ADMIN_ROLE
    
    
class EventPages(Enum):
    MAIN = "main"
    EVENT = "event"