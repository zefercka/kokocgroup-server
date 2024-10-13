import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    IMAGES_PATH: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )
    

class Transactions:
    #  If you change it here, then you can also change it in the database
    
    # Actions with news
    CREATE_NEWS = "create_news"
    EDIT_NEWS = "edit_news"
    DELETE_NEWS = "delete_news"
    VIEW_DELETED_NEWS = "view_deleted_news"
    VIEW_SHEDULED_NEWS = "view_sheduled_news"
    UPLOAD_IMAGE = "upload_image"
    
    # Actions with roles
    CREATE_ROLE = "create_role"
    EDIT_ROLE = "edit_role"
    DELETE_ROLE = "delete_role"
    
    # Add role to user
    ADD_ROLE = "add_role"
    # Remove role from user
    REMOVE_ROLE = "remove_role"
    
    # Actions with teams
    CREATE_TEAM = "create_team"
    EDIT_TEAM = "edit_team"
    DELETE_TEAM = "delete_team"
    
    # Actions with team mebers
    ADD_TEAM_MEMBER = "add_team_member"
    EDIT_TEAM_MEMBER = "edit_team_member"
    DELETE_TEAM_MEMBER = "delete_team_member"
    
    # Actions with locations
    CREATE_LOCATION = "create_location"
    EDIT_LOCATION = "edit_location"
    DELETE_LOCATION = "delete_location"
    
    # Actions with events
    CREATE_EVENT = "create_event"
    EDIT_EVENT = "edit_event"
    DELETE_EVENT = "delete_event"
    
    # Actions with store items
    CREATE_STORE_ITEM = "create_store_item"
    EDIT_STORE_ITEM = "create_store_item"
    DELETE_STORE_ITEM = "delete_store_item"
    
    
class TeamMemberSettings:
    #  If you change it here, then you can also change it in the database
    
    # Playing in the current squad
    PRESENT_STATUS = "present"
    # Played in the squad before
    PAST_STATUS = "past"
    
    # Team members roles
    ADMIN_ROLE = "admin"
    TRAINER_ROLE = "trainer"
    PLAYER_ROLE = "player"
    
    # Players positions
    GOALKEPPER_POSITION = "голкиппер"
    DEFENDER_POSITION = "защитник"
    MIDFIELDERS_POSITION = "полузащитник"
    STRIKER_POSITION = "нападающий"


class DBConstants:
    # Availability of news (if new was deleted, than it has NEWS_UNAVAILABLE)
    NEWS_AVAILABLE = "available"
    NEWS_UNAVAILABLE = "unavailable"
    
    # Name of base settings in table base_settings
    BASE_ROLE = "BASE_ROLE_ID"
    BASE_TEAM = "BASE_TEAM_ID"
    
    # The news is deleted automatically after the expiration DELETE_NEWS_AFTER
    DELETE_NEWS_AFTER = 7
    
    

settings = Settings()
transactions = Transactions()
team_member_settings = TeamMemberSettings()
db_constants = DBConstants()

def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")