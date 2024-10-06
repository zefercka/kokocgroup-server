from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import Role
from datetime import datetime


async def get_role_by_id(db: AsyncSession, role_id: int) -> Role | None:
    results = await db.execute(select(Role).where(Role.id == role_id))
    return results.scalars().first()


async def get_roles(db: AsyncSession, limit: int, offset: int) -> list[Role] | None:
    results = await db.execute(select(Role).order_by(Role.id).limit(limit).offset(offset))
    return results.scalars().all()


async def add_role(db: AsyncSession, name: str, access_level: int) -> Role | None:
    role = Role(name=name, access_level=access_level)
    db.add(role)
    await db.commit()
    await db.refresh(role)

    return role


async def update_role_access_level(db: AsyncSession, role: Role, access_level: int) -> Role:
    role.access_level = access_level
    await db.commit()
    
    return role
    

async def update_role_name(db: AsyncSession, role: Role, name: str) -> Role:
    role.name = name
    await db.commit()
    
    return role