from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependecies.database import get_db
from ..schemas.role import Role
from ..services import role_service

app = APIRouter()


@app.get("/", response_model=list[Role])
async def get_all_roles(limit: int = 0, offset: int = 0, db: AsyncSession = Depends(get_db)):
    roles = await role_service.get_roles(db, limit, offset)
    return roles


@app.post("/", response_model=Role)
async def create_role(role: Role, db: AsyncSession = Depends(get_db)):
    role = await role_service.create_role(db, role)
    return role 


@app.get("/{role_id}", response_model=Role)
async def get_role(role_id: int, db: AsyncSession = Depends(get_db)):
    role = await role_service.get_role(db, role_id=role_id)
    return role


@app.put("/{role_id}", response_model=Role)
async def update_role(role_id: int, name: str, db: AsyncSession = Depends(get_db)):
    if name is not None:
        role = await role_service.update_name(db, role_id=role_id, name=name)
        
    return role