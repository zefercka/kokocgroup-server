from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db
from app.api.schemas.role import CreateRole, Role
from app.api.schemas.user import User
from app.api.services import auth_service, roles_service

app = APIRouter()


@app.get("", response_model=list[Role])
async def get_all_roles(limit: int = 10, offset: int = 0, db: AsyncSession = Depends(get_db)):
    roles = await roles_service.get_roles(db, limit, offset)
    return roles


@app.post("", response_model=Role)
async def create_role(role: CreateRole, 
                      current_user: User = Depends(auth_service.get_current_user),
                      db: AsyncSession = Depends(get_db)):
    role = await roles_service.create_role(
        db, role=role, current_user=current_user
    )
    return role 


@app.get("/{role_id}", response_model=Role)
async def get_role(role_id: int, db: AsyncSession = Depends(get_db)):
    role = await roles_service.get_role(db, role_id=role_id)
    return role


@app.put("", response_model=Role)
async def edit_role(role: Role, 
                      current_user: User = Depends(auth_service.get_current_user),
                      db: AsyncSession = Depends(get_db)):
    role = await roles_service.edit_role(
        db, role=role, current_user=current_user
    )
        
    return role


@app.post("/{role_id}")
async def delete_role(role_id: int, 
                      current_user = Depends(auth_service.get_current_user),
                      db: AsyncSession = Depends(get_db)):
    await roles_service.delete_role(
        db, role_id=role_id, current_user=current_user
    )