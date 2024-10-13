from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import team_member_settings

from ..models import Location


@logger.catch
async def get_location_by_id(db: AsyncSession, location_id: int) -> Location:
    """
    Get a location from the database by its ID.

    Args:
        db (AsyncSession): The database session.
        location_id (int): The ID of the location to get.

    Returns:
        Location: The location if found, otherwise None.
    """

    results = await db.execute(
        select(Location).where(Location.id == location_id)
    )
    return results.scalars().first()


@logger.catch
async def get_all_locations(db: AsyncSession, limit: int, 
                            offset: int) -> list[Location]:
    """
    Get a list of all locations in the database.

    Args:
        db (AsyncSession): The database session.
        limit (int): The maximum number of locations to return.
        offset (int): The number of locations to skip.

    Returns:
        list[Location]: The list of locations.
    """
    
    results = await db.execute(
        select(Location).order_by(Location.id).offset(offset).limit(limit)
    )
    return results.scalars().all()


@logger.catch
async def create_location(db: AsyncSession, name: str, 
                          address: str) -> Location:
    """
    Create a new location in the database.

    Args:
        db (AsyncSession): The database session.
        name (str): The name of the location.
        address (str): The address of the location.

    Returns:
        Location: The created location.
    """
    
    location = Location(name=name, address=address)
    db.add(location)
    await db.commit()
    await db.refresh(location)

    return location


@logger.catch
async def edit_location(db: AsyncSession, location: Location, name: str, 
                        address: str) -> Location:
    """
    Edit a location in the database.

    Args:
        db (AsyncSession): The database session.
        location (Location): The location to edit.
        name (str): The new name of the location.
        address (str): The new address of the location.

    Returns:
        Location: The edited location.
    """
    
    location.name = name
    location.address = address
    await db.commit()
    await db.refresh(location)
    
    return location