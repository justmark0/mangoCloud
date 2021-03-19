from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, render
from django.http import HttpRequest, FileResponse, JsonResponse
from backend.models import User  # It is right import
from django.contrib.auth import authenticate
from .models import File, Folder, Access
from .services import *
from .forms import *
import json


@csrf_exempt
def get_file(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse("Specify files that you need to receive, and your token. Communicate with POST method")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return HttpResponse("Couldn't decode your json")
        if validate_json(data, token=True, file_id=True):
            user = get_or_none(User, token=data['token'])  # Validating token
            if user is None:
                return HttpResponse("Error. Update token")

            file = absolute_path_from_filename(data['file_id'])
            file_entry = get_or_none(File, file_id=data['file_id'])
            if file_entry is None or file is None:
                return HttpResponse("There is no such file")
            if file_entry.is_folder is True:
                return HttpResponse("It is folder")

            if file_entry.user_id != user:
                return HttpResponse("You have no rights to see this file")

            return FileResponse(open(file, 'rb'), filename=file_entry.file_name)
        return HttpResponse("Error. Check if file name (less 512) and token is less than 256 symbols and not none")
    return HttpResponse("API supprots only GET and POST methods")


@csrf_exempt
def upload_file(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse("Use method POST. token (max symbols 512) and file")
    if request.method == "POST":
        if validate_json(request.POST, token=True, file_name=True) and request.FILES['file'] is not None:
            user = get_or_none(User, token=request.POST['token'])  # Validating token
            if user is None:
                return HttpResponse("Error. Update token")

            file_entry = File.objects.create(file_id=get_unique_id(), file_name=request.POST['file_name'], user_id=user)
            save_file_in_folder(name=file_entry.file_id, file=request.FILES['file'])
            response = {"file_id": file_entry.file_id}
            return HttpResponse(json.dumps(response))
        return HttpResponse("Request is invalid. Check that you sent file, token (less than 256), file_name (less "
                            "than 512) and not none")
    return HttpResponse("API supports only GET and POST methods")


@csrf_exempt
def get_token(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse("Use method POST. username and password in plain text")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return HttpResponse("Couldn't decode your json")
        if validate_json(data, username=True, password=True):
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is None:
                return json_error("This user already exists")
            user.get_new_token()
            user.save()
            return JsonResponse({"token": user.token}, safe=False)
        return json_error("Wrong format")
    return HttpResponse("API supports only GET and POST methods")


@csrf_exempt
def reg_view(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse("Use post method and specify your username and password")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return HttpResponse("Couldn't decode your json")
        if validate_json(data, username=True, password=True):
            user_exist = get_or_none(User, username=data['username'])
            if user_exist is not None:
                return json_error("Error. User with this username alerady exists")
            instance = User(username=data['username'])
            instance.get_new_token()
            instance.set_password(data['password'])
            instance.save()
            return JsonResponse({"token": instance.token}, safe=False)
        return HttpResponse("Username (less that 150) and password (less than 50) should be not none")
    return HttpResponse("Site supprots only GET and POST methods")


@csrf_exempt
def folder_content_view(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse("Use post method and specify your username and password")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return HttpResponse("Couldn't decode your json")
        if validate_json(data, token=True, file_id=True):
            user = get_or_none(User, token=data['token'])  # Validating token
            if user is None:
                return HttpResponse("Error. Update token")

            if not has_access(user=user, file_id=data['file_id']):
                return HttpResponse("You do not have accsess to this file/folder")

            fold = get_or_none(File, file_id=data['file_id'])
            if fold.is_folder is False:
                return HttpResponse("This is file, not folder")

            files = []
            buff_list = list(Folder.objects.filter(folder=fold))
            for el in buff_list:
                files.append({"file_id": el.file.file_id, "is_folder": el.file.is_folder})

            return JsonResponse(files, safe=False)
        return json_error("Wrong credentials")
    return json_error("Site supprots only GET and POST methods")


@csrf_exempt
def grand_accsess_view(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse("Use post method and specify your username and password")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return HttpResponse("Couldn't decode your json")
        if validate_json(data, token=True, file_id=True, username=True, can_edit=True):
            user = validate_user(data, check_owner=True)
            if str(type(user)) == "<class 'str'>":
                return json_error(str(user))

            share_uid = get_or_none(User, username=data['username'])
            if share_uid is None:
                return json_error("There is no such user")

            can_edit = data['can_edit'] == 'True'
            Access(file_id=data['file_id'], owner_id=user, share_uid=share_uid, can_edit=can_edit).save()
            return JsonResponse({"message": "successful"})
        return json_error("Wrong credentials")
    return json_error("Site supprots only GET and POST methods")


@csrf_exempt
def create_dir(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse("Use post method and specify your token, file_name (folder name)")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return HttpResponse("Couldn't decode your json")
        if validate_json(data, token=True, file_name=True):
            user = validate_user(data)
            if str(type(user)) == "<class 'str'>":
                return json_error(str(user))

            fold_file = File.objects.create(file_id=get_unique_id(), user_id=user, is_folder=True,
                                            file_name=data['file_name'])

            return JsonResponse({"file_id": fold_file.file_id})
        return json_error("Wrong credentials")
    return json_error("Site supprots only GET and POST methods")


@csrf_exempt
def move_file_to_dir(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse("Use post method and specify your token, file_id ( and password")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return HttpResponse("Couldn't decode your json")
        if validate_json(data, token=True, file_id=True, fold_id=True):
            user = validate_user(data, check_owner=True, check_owner_folder=True)
            if str(type(user)) == "<class 'str'>":
                return json_error(str(user))

            folder_entry = get_or_none(File, file_id=data['fold_id'])
            if folder_entry is None:
                return HttpResponse("There os no such folder")
            if folder_entry.is_folder is False:
                return HttpResponse(f"{data['fold_id']} is not a folder")

            file_entry = get_or_none(File, file_id=data['file_id'])
            if file_entry is None:
                return HttpResponse("There os no such file")

            old_folder = get_or_none(Folder, file=file_entry)
            if old_folder is not None:
                old_folder.delete()

            Folder(folder=folder_entry, file=file_entry).save()

            return JsonResponse({"message": "success"})
        return json_error("Wrong credentials")
    return json_error("Site supprots only GET and POST methods")