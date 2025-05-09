from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models import Team


@logger.catch
async def get_team_by_id(db: AsyncSession, team_id: int) -> Team:
    results = await db.execute(select(Team).where(Team.id == team_id))
    return results.scalars().first()


@logger.catch
async def get_all_teams(db: AsyncSession, limit: int, offset: int):
    results = await db.execute(
        select(Team).order_by(Team.id).limit(limit).offset(offset)
    )
    return results.scalars().all()


@logger.catch
async def create_team(db: AsyncSession, name: str, logo_url: str) -> Team:
    team = Team(name=name, logo_url=logo_url)
    db.add(team)
    await db.commit()
    await db.refresh(team)
    
    return team


@logger.catch
async def edit_team(db: AsyncSession, team: Team, name: str, 
                    logo_url: str) -> Team:
    team.name = name
    team.logo_url = logo_url
    await db.commit()
    await db.refresh(team)
    
    return team


@logger.catch
async def delete_team(db: AsyncSession, team: Team):
    await db.delete(team)
    await db.commit()