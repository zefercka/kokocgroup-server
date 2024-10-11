from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependecies.database import get_db
from ..schemas.user import SendUser, User
from ..services import auth_service, users_service

app = APIRouter()

@app.get("/{user_id}", response_model=SendUser)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await users_service.get_user(db, user_id)
    return user


@app.get("", response_model=list[SendUser])
async def get_users(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    users = await users_service.get_all_users(db, limit, offset)
    return users
        
    
@app.post("/{user_id}/roles/{role_id}")
async def add_role_to_user(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)):
    user = await users_service.add_role_to_user(db, user_id, role_id)
    return user
    

@app.delete("/{user_id}/roles/{role_id}", response_model=SendUser)
async def remove_role_user(user_id: int, role_id: int, current_user: User = Depends(auth_service.get_current_user), 
                           db: AsyncSession = Depends(get_db)):
    user = await users_service.remove_role_user(
        db, current_user=current_user, user_id=user_id, role_id=role_id
    )
    return user


# Delete after
# @app.post("/permission")
# async def add_permission(user_id: int, permission_id: int, db: AsyncSession = Depends(get_db)):
    