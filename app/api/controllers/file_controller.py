from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependecies.database import get_db
from ..schemas.user import User
from ..services import auth_service, file_service

app = APIRouter()


@app.post("/images", response_model=str)
async def upload_image(image: UploadFile, current_user: User = Depends(auth_service.get_current_user),
                       db: AsyncSession = Depends(get_db)):
    file_name = await file_service.upload_image(db, image=image, current_user=current_user)
    return file_name
    

@app.get("/images/{file_name}", response_class=FileResponse)
async def get_image(file_name: str):
    file = await file_service.get_image(file_name)
    return file
    