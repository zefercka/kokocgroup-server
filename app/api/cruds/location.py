from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import team_member_settings

from ..models import Location


async def get_location_by_id(db: AsyncSession, location_id: int) -> Location:
    results = await db.execute(
        select(Location).where(Location.id == location_id)
    )
    return results.scalars().first()


async def get_all_locations(db: AsyncSession, limit: int, 
                            offset: int) -> list[Location]:
    results = await db.execute(
        select(Location).order_by(Location.id).offset(offset).limit(limit)
    )
    return results.scalars().all()


async def create_location(db: AsyncSession, name: str, 
                          address: str) -> Location:
    location = Location(name=name, address=address)
    db.add(location)
    await db.commit()
    await db.refresh(location)

    return location


async def edit_location(db: AsyncSession, location: Location, name: str, 
                        address: str) -> Location:
    location.name = name
    location.address = address
    await db.commit()
    await db.refresh(location)
    
    return location