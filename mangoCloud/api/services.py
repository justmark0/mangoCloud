from django.conf import settings
from random import randint
from hashlib import sha256
from .models import File


def get_or_none(classname, **kwargs):
    try:
        return classname.objects.get(**kwargs)
    except classname.DoesNotExist:
        return None


def absolute_path_from_filename(name: str):
    path = (settings.FILES_FOLDER / name)
    if not path.exists():
        return None
    return str(path)


def create_file_id():
    while True:
        a = str(randint(0, int(1e9))) + str(randint(0, int(1e9)))
        h = sha256(a.encode()).hexdigest()
        file = get_or_none(File, file_id=h)
        if file is None:
            return a


def save_file_in_folder(name: str, file):
    with open(str(settings.FILES_FOLDER / name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
