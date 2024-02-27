from django.core.files.storage import FileSystemStorage
import os

from django.core.files.storage import default_storage
def upload_file(image):
    fs = FileSystemStorage()
    # img_name = image.name
    file = fs.save(image.name, image)
    file_url = fs.url(file)
    # print(file_url)
    return f"{os.getcwd()}/media/{image.name}"