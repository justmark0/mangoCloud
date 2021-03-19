from django.http import JsonResponse
from django.conf import settings
from random import randint
from hashlib import sha256
from .models import File
import json


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


def get_unique_id(classname=File):
    while True:
        a = str(randint(0, int(1e9))) + str(randint(0, int(1e9)))
        h = sha256(a.encode()).hexdigest()
        if classname == File:
            entry = get_or_none(classname, file_id=h)
        elif str(classname) == "<class 'backend.models.User'>":
            entry = get_or_none(classname, token=h)
        else:
            return
        if entry is None:
            return h


def save_file_in_folder(name: str, file):
    with open(str(settings.FILES_FOLDER / name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def field_json_is_valid(data, field, max_length=256):
    if field in data.keys():
        if 0 < len(data[field]) <= max_length:
            return True
    return False


def validate_json(data, token=False, file_id=False, file_name=False, username=False, password=False):
    if token is True:
        if not field_json_is_valid(data, 'token', 256):
            return False
    if file_id is True:
        if not field_json_is_valid(data, 'file_id', 256):
            return False
    if file_name is True:
        if not field_json_is_valid(data, 'file_name', 512):
            return False
    if username is True:
        if not field_json_is_valid(data, 'username', 150):
            return False
    if password is True:
        if not field_json_is_valid(data, 'password', 50):
            return False
    return True


def json_error(message):
    return JsonResponse({"Error": message})
