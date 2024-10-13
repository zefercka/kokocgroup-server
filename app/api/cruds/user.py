from datetime import date

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependecies import hash
from ..models import Role, User


@logger.catch
async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    results = await db.execute(select(User).where(User.id == user_id))
    return results.scalars().first()


@logger.catch
async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    results = await db.execute(select(User).where(User.username == username))
    return results.scalars().first()


@logger.catch
async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    results = await db.execute(select(User).where(User.email == email))
    return results.scalars().first()


@logger.catch
async def get_users(db: AsyncSession, limit: int = 50, offset: int = 0) -> User | None:
    results = await db.execute(
        select(User).order_by(User.id).limit(limit).offset(offset)
    )
    return results.scalars().all()


@logger.catch
async def add_user(db: AsyncSession, username: str, email: str, first_name: str, last_name: str, 
                   date_of_birth: date, password: str, patronymic: str | None = None, 
                   phone_number: str | None = None, avatar_url: str | None = None):
    password_hash = await hash.get_password_hash(password)
    user = User(
        username=username, email=email, first_name=first_name, last_name=last_name, 
        date_of_birth=date_of_birth, patronymic=patronymic, password_hash=password_hash,
        phone_number=phone_number, avatar_url=avatar_url)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


@logger.catch
async def add_role_to_user(db: AsyncSession, user: User, role: Role) -> User:
    user.roles.append(role)
    await db.commit()
    await db.refresh(user)
    
    return user


@logger.catch
async def remove_role_user(db: AsyncSession, user: User, role: Role) -> User:
    user.roles.remove(role)
    await db.commit()
    await db.refresh(user)
    
    return user