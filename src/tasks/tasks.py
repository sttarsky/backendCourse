import os.path
from time import sleep
from src.tasks.celery_app import celery_instance
from PIL import Image

@celery_instance.task
def test_task():
    sleep(3)
    print("Test celery")


@celery_instance.task
def resize_image(image_path):
    sizes = [1000, 500, 200]
    output_folder = 'src/static/images'
    img = Image.open(image_path)

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        img_resized = img.resize((size, int(img.height * (size/img.width))), Image.Resampling.LANCZOS)

        new_file_name = f"{name}_{size}px{ext}"

        output_path = os.path.join(output_folder, new_file_name)
        # Сохраняем изображение
        img_resized.save(output_path)


