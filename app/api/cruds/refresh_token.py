from datetime import datetime

from loguru import logger
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models import RefreshToken


@logger.catch
async def get_token(db: AsyncSession, token: str) -> RefreshToken | None:
    """
    Get a RefreshToken object by its token string.

    Args:
        db: The database session.
        token: The token string to search for.

    Returns:
        The RefreshToken object if found, or None if not found.
    """

    results = await db.execute(
        select(RefreshToken).where(RefreshToken.token == token)
    )
    return results.scalars().first()


@logger.catch
async def delete_token_obj(db: AsyncSession, token: RefreshToken):
    """
    Delete a RefreshToken object.

    Args:
        db: The database session.
        token: The RefreshToken object to delete.
        
    Returns:
        None
    """
    await db.delete(token)
    await db.commit()


@logger.catch
async def delete_token(db: AsyncSession, token: str):
    """
    Delete a RefreshToken object by its token string.

    Args:
        db: The database session.
        token: The token string to delete.

    Returns:
        None
    """
    token_obj = await get_token(db, token)
    if token_obj is not None:
        await delete_token_obj(db, token_obj)


@logger.catch
async def add_token(db: AsyncSession, token: str, expired_date: datetime, user_id: int):
    """
    Add a new RefreshToken to the database.

    Args:
        db: The database session.
        token: The token string.
        expired_date: The datetime of the token's expiration.
        user_id: The ID of the user that this token belongs to.

    Returns:
        RefreshToken: The newly created RefreshToken object.
    """
    db_token = RefreshToken(
        token=token, expire_date=expired_date.replace(tzinfo=None), user_id=user_id
    )
    db.add(db_token)
    await db.commit()
    await db.refresh(db_token)
    return db_token


@logger.catch
async def delete_expired_tokens(db: AsyncSession):
    """
    Delete all expired RefreshTokens from the database.

    Args:
        db: The database session.

    Returns:
        None
    """
    await db.execute(
        delete(RefreshToken).where(RefreshToken.expire_date < datetime.now())
    )
    await db.commit()    