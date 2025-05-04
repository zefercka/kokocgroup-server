from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db
from app.api.schemas.location import CreateLocation, Location
from app.api.schemas.user import User
from app.api.services import locations_service
from app.api.services.auth_service import get_current_user

app = APIRouter()


@app.get("", response_model=list[Location])
async def get_all_locations(limit: int = 10, offset: int = 0, 
                            db: AsyncSession = Depends(get_db)):
    locations = await locations_service.get_all_locations(
        db, limit=limit, offset=offset
    ) 
            
    return locations


@app.get("/{location_id}", response_model=Location)
async def get_location(location_id: int, db: AsyncSession = Depends(get_db)):
    location = await locations_service.get_location(
        db, location_id=location_id
    )
    return location


@app.post("", response_model=Location)
async def create_location(location: CreateLocation, 
                           current_user: User = Depends(get_current_user), 
                           db: AsyncSession = Depends(get_db)):
    return await locations_service.create_location(
        db, location=location, current_user=current_user
    )
    
    
@app.put("", response_model=Location)
async def edit_location(location: Location, 
                        current_user: User = Depends(get_current_user), 
                        db: AsyncSession = Depends(get_db)):
    return await locations_service.edit_location(
        db, location=location, current_user=current_user
    )