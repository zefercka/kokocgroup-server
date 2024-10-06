from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import Role
from ..cruds.role import add_role, get_role_by_id, update_role_access_level, update_role_name
from ..dependecies.exceptions import RoleNotFound

async def create_role(db: AsyncSession, role: Role) -> Role:
    role = await add_role(db, name=role.name, access_level=role.access_level)
    return role


async def get_roles(db: AsyncSession, limit: int, offset: int) -> list[Role]:
    roles = await get_roles(db, limit=limit, offset=offset)
    return roles


async def update_access_level(db: AsyncSession, role_id: int, access_level: int) -> Role:
    role = await get_role_by_id(db, role_id)
    if role is None:
        raise RoleNotFound
    
    role = await update_role_access_level(db, role, access_level)
    return role


async def update_name(db: AsyncSession, role_id: int, name: str) -> Role:
    role = await get_role_by_id(db, role_id)
    if role is None:
        raise RoleNotFound
    
    role = await update_role_name(db, role, name)
    return role