from sqlalchemy.ext.asyncio import AsyncSession

from ..models import FileUpload


async def add_image(db: AsyncSession, file_name: str, user_id: int):
    image = FileUpload(file_name=file_name, user_id=user_id)
    db.add(image)
    await db.commit()
