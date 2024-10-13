import os
import uuid

from fastapi import UploadFile
from fastapi.responses import FileResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings, transactions

from ..cruds import files as crud
from ..dependecies.exceptions import (FileNotFound, InternalServerError,
                                      UnexpectedFileType)
from ..dependecies.images_compressor import compress_and_save_image
from ..schemas.user import User
from . import users_service


async def upload_image(db: AsyncSession, image: UploadFile, current_user: User):
    await users_service.check_user_permission(
        current_user, transactions.UPLOAD_IMAGE
    )
        
    if image.content_type.split('/')[0] != "image":
        raise UnexpectedFileType

    try:
        file_path = os.getcwd() + settings.IMAGES_PATH + str(uuid.uuid4())
        while os.path.exists(file_path):
            file_path = os.getcwd() + settings.IMAGES_PATH + str(uuid.uuid4())
            
        path = await compress_and_save_image(image=image, path=file_path)
        file_name = path.split("/")[-1]

        await crud.add_image(db, file_name=file_name, user_id=current_user.id)
        await image.close()

        return file_name
    except Exception as err:
        logger.error(err)
        raise InternalServerError
    

async def get_image(file_name: str):
    file_path = os.getcwd() + settings.IMAGES_PATH + file_name
    if not os.path.exists(file_path):
        raise FileNotFound
    
    return FileResponse(file_path)
    