from django.core.files.storage import FileSystemStorage
from django.conf import settings
from urllib.parse import urljoin
import os
from django.utils.timezone import now

class CustomStorage(FileSystemStorage):
    location = os.path.join(
        settings.MEDIA_ROOT,
        "ckeditor5",
        str(now().year),
        f"{now().month:02d}",
        f"{now().day:02d}"
    )
    base_url = urljoin(
        settings.MEDIA_URL,
        f"ckeditor5/{now().year}/{now().month:02d}/{now().day:02d}/"
    )