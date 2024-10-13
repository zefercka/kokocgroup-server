from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Role
from loguru import logger


@logger.catch
async def get_role_by_id(db: AsyncSession, role_id: int) -> Role | None:
    results = await db.execute(select(Role).where(Role.id == role_id))
    return results.scalars().first()


@logger.catch
async def get_roles(db: AsyncSession, limit: int, offset: int) -> list[Role] | None:
    results = await db.execute(
        select(Role).order_by(Role.id).limit(limit).offset(offset)
    )
    return results.scalars().all()


@logger.catch
async def create_role(db: AsyncSession, name: str) -> Role | None:
    role = Role(name=name)
    db.add(role)
    await db.commit()
    await db.refresh(role)

    return role
    

@logger.catch
async def update_role_name(db: AsyncSession, role: Role, name: str) -> Role:
    role.name = name
    await db.commit()
    
    return role


@logger.catch
async def delete_role(db: AsyncSession, role: Role):
    await db.delete(role)
    await db.commit()