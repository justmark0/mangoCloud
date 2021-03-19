from backend.models import User  # It is right import
from django.http import JsonResponse
from .models import File, Access
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


def validate_json(data, token=False, file_id=False, file_name=False, username=False, password=False, can_edit=False,
                  fold_id=False):
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
    if can_edit is True:
        if not field_json_is_valid(data, 'can_edit', 5):
            return False
    if fold_id is True:
        if not field_json_is_valid(data, 'fold_id', 256):
            return False
    return True


def json_error(message):
    return JsonResponse({"Error": message}, safe=False)


def has_access(user, file_id):
    file = get_or_none(File, file_id=file_id)
    has = get_or_none(Access, file_id=file, share_uid=user)
    if has is None:
        if file.user_id != user:
            return False
    return True


def validate_user(data, check_accsess=False, check_owner=False, check_owner_folder=False):
    user = get_or_none(User, token=data['token'])  # Validating token
    if user is None:
        return "Error. Update token"
    if check_accsess is True:
        if not has_access(user, data['file_id']):
            return "You do not have accsess to this file/folder"
    if check_owner is True:
        file = get_or_none(File, user_id=user, file_id=data['file_id'])
        if file is None:
            return "No such file or you don't have acsess"
    if check_owner_folder is True:
        file = get_or_none(File, user_id=user, file_id=data['fold_id'])
        if file is None:
            return "No such fold or you don't have acsess"

    return user
