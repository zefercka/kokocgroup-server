from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependecies.database import get_db
from ..schemas.team import Team
from ..services import auth_service, team_service
from app.config import team_member_settings

app = APIRouter()


@app.get("", response_model=Team)
async def get_team_members(status: str = "present", db: AsyncSession = Depends(get_db)):
    if status == team_member_settings.PRESENT_STATUS:
        members = await team_service.get_all_active_team_members(db)
    elif status == team_member_settings.PAST_STATUS:
        members = await team_service.get_all_inactive_team_members(db)
    else:
        members = []   
            
    return members


# @app.post("")


# @app.get("/", )
# async def 