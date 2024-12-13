from fastapi import APIRouter, UploadFile, BackgroundTasks
from src.tasks.tasks import resize_image
import shutil

router = APIRouter(prefix='/images', tags=['Изображения отелей'])


@router.post("")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(fsrc=file.file, fdst=new_file)
    background_tasks.add_task(resize_image, image_path)
    # resize_image.delay(image_path)
