from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependecies.database import get_db
from ..dependecies.enums import ImageFormats
from ..schemas.user import User
from ..services import auth_service, files_service

app = APIRouter()


@app.post("/images", response_model=str)
async def upload_image(image: UploadFile, 
                       format: ImageFormats = ImageFormats.JPG,
                       current_user: User = Depends(auth_service.get_current_user),
                       db: AsyncSession = Depends(get_db)):
    file_name = await files_service.upload_image(
        db, image=image, current_user=current_user, format=format
    )
    return file_name
    

@app.get("/images/{file_name}", response_class=FileResponse)
async def get_image(file_name: str):
    file = await files_service.get_image(file_name)
    return file
    