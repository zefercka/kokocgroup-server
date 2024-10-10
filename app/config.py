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
    CREATE_NEWS = "create_news"
    EDIT_NEWS = "edit_news"
    DELETE_NEWS = "delete_news"
    UPLOAD_IMAGE = "upload_image"
    
    CREATE_ROLE = "create_role"
    EDIT_ROLE = "edit_role"
    DELETE_ROLE = "delete_role"
    
    ADD_ROLE = "add_role"
    REMOVE_ROLE = "remove_role"
    
    VIEW_DELETED_NEWS = "view_deleted_news"
    VIEW_SHEDULED_NEWS = "view_sheduled_news"
    

class TeamMemberSettings:
    # Играют в текущем составе
    PRESENT_STATUS = "present"
    # Были в составе раннее, но сейчас не играют
    PAST_STATUS = "past"
    
    ADMIN_ROLE = "admin"
    TRAINER_ROLE = "trainer"
    PLAYER_ROLE = "player"
    
    GOALKEPPER_POSITION = "голкиппер"
    DEFENDER_POSITION = "защитник"
    MIDFIELDERS_POSITION = "полузащитник"
    STRIKER_POSITION = "нападающий"


class DB_CONSTANTS:
    NEWS_AVAILABLE = "available"
    NEWS_UNAVAILABLE = "unavailable"
    
    BASE_ROLE = "BASE_ROLE_ID"
    
    

settings = Settings()
transactions = Transactions()
team_member_settings = TeamMemberSettings()
db_constants = DB_CONSTANTS()

def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")