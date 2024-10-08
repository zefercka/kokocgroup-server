from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import RefreshToken


async def get_token(db: AsyncSession, token: str):
    results = await db.execute(select(RefreshToken).where(RefreshToken.token == token))
    return results.scalars().first()


async def delete_token_obj(db: AsyncSession, token: RefreshToken):
    await db.delete(token)
    await db.commit()


async def delete_token(db: AsyncSession, token: str):
    token_obj = await get_token(db, token)
    if token_obj is not None:
        await delete_token_obj(db, token_obj)


async def add_token(db: AsyncSession, token: str, expired_date: datetime, user_id: int):
    db_token = RefreshToken(
        token=token, expire_date=expired_date.replace(tzinfo=None), user_id=user_id
    )
    db.add(db_token)
    await db.commit()
    await db.refresh(db_token)
    return db_token