from django.core.files.storage import FileSystemStorage
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent


class CustomStorage(FileSystemStorage):
    location = os.path.join(BASE_DIR, "ckeditor5")
    base_url = "/ckeditor5/"