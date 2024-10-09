from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependecies.database import get_db
from ..schemas.team import Team
from ..services import auth_service, team_service
from app.config import team_member_settings

app = APIRouter()


@app.get("/", response_model=Team)
async def get_team_members(status: str = "active", db: AsyncSession = Depends(get_db)):
    members = await team_service.get_all_active_team_members(db)
    return members


# @app.get("/", )
# async def 