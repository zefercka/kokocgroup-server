from PIL import Image
from fastapi import UploadFile

TARGET_SIZE_MB = 5


async def compress_and_save_image(image: UploadFile, path: str):
    img = Image.open(image.file)
    img = img.convert("RGB")
    
    target_size = TARGET_SIZE_MB * 1024 * 1024
    
    if image.size > target_size:
        ratio = (target_size / image.size) ** 0.5
        img = img.resize(
            (round(img.size[0] * ratio), round(img.size[1] * ratio))
        )
    
    path = path + ".jpg"
    img.save(path, format="JPEG")
    img.close()
    await image.close()
    
    return path