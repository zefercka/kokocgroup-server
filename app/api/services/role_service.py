from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.role import Role
from ..cruds import role as crud 
from ..dependecies.exceptions import RoleNotFound


async def create_role(db: AsyncSession, role: Role) -> Role:
    role = await crud.add_role(db, name=role.name)
    return Role.model_validate(role)


async def get_roles(db: AsyncSession, limit: int, offset: int) -> list[Role]:
    roles = await get_roles(db, limit=limit, offset=offset)
    return roles


async def update_name(db: AsyncSession, role_id: int, name: str) -> Role:
    role = await crud.get_role_by_id(db, role_id)
    if role is None:
        raise RoleNotFound
    
    role = await crud.update_role_name(db, role, name)
    return Role.model_validate(role)