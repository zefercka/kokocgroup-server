from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import FileUpload


@logger.catch
async def add_image(db: AsyncSession, file_name: str, user_id: int):
    """
    Add a info about new image to the database.

    Args:
        db (AsyncSession): The database session.
        file_name (str): The name of the image file.
        user_id (int): The ID of the user that uploaded the image.
    """
    image = FileUpload(file_name=file_name, user_id=user_id)
    db.add(image)
    await db.commit()
