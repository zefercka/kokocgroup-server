from fastapi import UploadFile
from loguru import logger
from PIL import Image

from app.api.dependencies.enums import ImageFormats

TARGET_SIZE_MB = 5


@logger.catch
async def compress_and_save_image(image: UploadFile, path: str, 
                                  format: ImageFormats):
    img = Image.open(image.file)
    
    if format == ImageFormats.JPG:
        img = img.convert("RGB")
    
    target_size = TARGET_SIZE_MB * 1024 * 1024
    
    if image.size > target_size:
        ratio = (target_size / image.size) ** 0.5
        img = img.resize(
            (round(img.size[0] * ratio), round(img.size[1] * ratio))
        )
    
    if format == ImageFormats.JPG:
        path = path + ".jpg"
        img.save(path, format="JPEG")
    elif format == ImageFormats.PNG:
        path = path + ".png"
        img.save(path, format="PNG")
        
    img.close()
    await image.close()
    
    return path