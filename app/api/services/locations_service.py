from sqlalchemy.ext.asyncio import AsyncSession

from app.config import transactions

from .. import models
from ..cruds import location as crud
from ..dependecies.exceptions import LocationNotFound
from ..schemas.location import Location, CreateLocation
from ..schemas.user import User
from ..services.users_service import check_user_permission


async def get_all_locations(db: AsyncSession, limit: int, 
                            offset: int) -> list[Location]:
    location_objs = await crud.get_all_locations(db, limit=limit, offset=offset)
    locations = [
        Location.model_validate(location) for location in location_objs
    ]
    
    return locations
    
    
async def get_location(db: AsyncSession, location_id: int) -> Location:
    location = await crud.get_location_by_id(db, location_id)
    if location is None:
        raise LocationNotFound
    return Location.model_validate(location)


async def create_location(db: AsyncSession, location: CreateLocation,
                          current_user: User) -> Location:
    await check_user_permission(current_user, transactions.CREATE_LOCATION)
    
    location = await crud.create_location(
        db, name=location.name, address=location.address
    )
    return Location.model_validate(location)


async def edit_location(db: AsyncSession, location: Location, 
                        current_user: User) -> Location:
    await check_user_permission(current_user, transactions.EDIT_LOCATION)
    
    location_obj = await crud.get_location_by_id(
        db, location_id=location.id
    )
    if location_obj is None:
        raise LocationNotFound
    
    location = await crud.edit_location(
        db, location=location_obj, name=location.name, address=location.address
    )
    return Location.model_validate(location)