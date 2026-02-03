import os
import glob
from fastapi import UploadFile, HTTPException
from app.config import settings

ALLOWED_IMAGE_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
}


def save_user_image(
    file: UploadFile,
    user_id: int,
    image_type: str,
) -> str:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image type")

    ext = ALLOWED_IMAGE_TYPES[file.content_type]
    filename = f"{user_id}_{image_type}.{ext}"

    old_files = glob.glob(f"{settings.images_dir}/{user_id}_{image_type}.*")
    for old_file in old_files:
        os.remove(old_file)

    file_path = os.path.join(settings.images_dir, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return f"/static/images/{filename}"
