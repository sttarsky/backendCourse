from fastapi import APIRouter, UploadFile
from src.tasks.tasks import resize_image
import shutil

router = APIRouter(prefix='/images', tags=['Изображения отелей'])


@router.post("")
def upload_image(file: UploadFile):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(fsrc=file.file, fdst=new_file)

    resize_image.delay(image_path)
