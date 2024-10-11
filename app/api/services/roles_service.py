from sqlalchemy.ext.asyncio import AsyncSession

from app.config import transactions

from ..cruds import permission as p_crud
from ..cruds import role as crud
from ..dependecies.exceptions import RoleNotFound
from ..schemas.role import CreateRole, Role
from ..schemas.user import User
from ..services.users_service import check_user_permission


async def create_role(db: AsyncSession, role: CreateRole, 
                      current_user: User) -> Role:
    await check_user_permission(current_user, transactions.CREATE_ROLE)
    
    created_role = await crud.create_role(db, name=role.name)
    created_role = await p_crud.add_permissions_to_role(
        db, permissons=role.permissions, role=created_role
    )
    return Role(
        id=created_role.id, name=created_role.name, 
        permissions=created_role.permissions
    )


async def get_roles(db: AsyncSession, limit: int, offset: int) -> list[Role]:
    roles = await crud.get_roles(db, limit=limit, offset=offset)
    return roles


async def edit_role(db: AsyncSession, role: Role, 
                    current_user: User) -> Role:
    await check_user_permission(current_user, transactions.EDIT_ROLE)
    
    existing_role = await crud.get_role_by_id(db, role.id)
    if existing_role is None:
        raise RoleNotFound
    
    if role.name != existing_role.name:
        existing_role = await crud.update_role_name(db, existing_role, role.name)
    
    existing_role_validated = Role(
        id=existing_role.id, name=existing_role.name, 
        permissions=existing_role.permissions
    )
    
    new_permissions = list(
        set(role.permissions) - set(existing_role_validated.permissions)
    )
    if new_permissions != []:
        existing_role = await p_crud.add_permissions_to_role(
            db, permissons=new_permissions, role=existing_role
        )
    
    existing_role_validated = Role(
        id=existing_role.id, name=existing_role.name, 
        permissions=existing_role.permissions
    )
    removed_permissions = list(
        set(existing_role_validated.permissions) - set(role.permissions)
    )
    if removed_permissions != []:
        existing_role = await p_crud.remove_peremissions_from_role(
            db, permissions=removed_permissions, role=existing_role
        )
    
    return Role(
        id=existing_role.id, name=existing_role.name, 
        permissions=existing_role.permissions
    )
    
    
async def get_role(db: AsyncSession, role_id: int) -> Role:
    role = await crud.get_role_by_id(db, role_id)
    if role is None:
        raise RoleNotFound
    
    return role


async def delete_role(db: AsyncSession, role_id: int, current_user: User):
    await check_user_permission(current_user, transactions.DELETE_ROLE)
    
    role = await crud.get_role_by_id(db, role_id=role_id)
    if role is None:
        raise RoleNotFound
    
    await crud.delete_role(db, role=role)