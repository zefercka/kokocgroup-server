from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models import Permission, Role


@logger.catch
async def get_permission(db: AsyncSession, permission: str) -> Permission:
    results = await db.execute(
        select(Permission).where(Permission.name == permission)
    )
    return results.scalars().first()


@logger.catch
async def get_permissions(db: AsyncSession, 
                          permissions: list[str]) -> list[Permission]:
    results = await db.execute(
        select(Permission).where(Permission.name.in_(permissions))
    )
    return results.scalars().all()


@logger.catch
async def add_permissions_to_role(db: AsyncSession, 
                                  permissons: list[str], role: Role) -> Role:
    permissons = await get_permissions(
        db, permissions=permissons
    )
    
    role.permissions.extend(permissons)
    await db.commit()
    await db.refresh(role)
    return role


@logger.catch
async def remove_peremissions_from_role(db: AsyncSession, 
                                       permissions: list[str], 
                                       role: Role) -> Role:
    permissions_objs = await get_permissions(
        db, permissions=permissions
    )
    role.permissions = list(set(role.permissions) - set(permissions_objs))
    await db.commit()
    await db.refresh(role)
    return role