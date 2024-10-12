from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Team


async def get_team_by_id(db: AsyncSession, team_id: int) -> Team:
    results = await db.execute(select(Team).where(Team.id == team_id))
    return results.scalars().first()


async def get_all_teams(db: AsyncSession, limit: int, offset: int):
    results = await db.execute(
        select(Team).order_by(Team.id).limit(limit).offset(offset)
    )
    return results.scalars().all()


async def create_team(db: AsyncSession, name: str, logo_url: str) -> Team:
    team = Team(name=name, logo_url=logo_url)
    db.add(team)
    await db.commit()
    await db.refresh(team)
    
    return team


async def edit_team(db: AsyncSession, team: Team, name: str, 
                    logo_url: str) -> Team:
    team.name = name
    team.logo_url = logo_url
    await db.commit()
    await db.refresh(team)
    
    return team


async def delete_team(db: AsyncSession, team: Team):
    await db.delete(team)
    await db.commit()