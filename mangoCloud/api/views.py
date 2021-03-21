import json
from _thread import *

from backend.models import User  # It is right import
from django.contrib.auth import authenticate
from django.http import HttpRequest, FileResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

from .services import *

LIMIT_MEMORY = int(1e8)


@csrf_exempt
def get_file(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse("Specify files that you need to receive, and your token. Communicate with POST method")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return json_error("Couldn't decode your json request")
        if validate_json(data, token=True, file_id=True):
            user = get_or_none(User, token=data['token'])  # Validating token
            if user is None:
                return json_error("Error. Update token")

            file = absolute_path_from_filename(data['file_id'] + ".7z")
            file_entry = get_or_none(File, file_id=data['file_id'])
            if file_entry is None or file is None:
                return json_error("There is no such file")
            if file_entry.is_folder is True:
                return json_error("It is folder")

            if not has_access(user, file_entry.file_id):
                return json_error("You have no rights to see this file")

            archive = py7zr.SevenZipFile(file, mode='r')
            archive.extractall(path=file[:-3:])
            archive.close()

            start_new_thread(delete_file_after_5s, (file[:-3:],))

            return FileResponse(open(str(file[:-3:] + "/" + file_entry.file_id), 'rb'), filename=file_entry.file_name)
        return json_error("Error. Check if file name (less 512) and token is less than 256 symbols and not none")
    return json_error("API supprots only GET and POST methods")


@csrf_exempt
def upload_file(request: HttpRequest):
    if request.method == "GET":
        return json_error("Use method POST. token (max symbols 512) and file")
    if request.method == "POST":
        if validate_json(request.POST, token=True, file_name=True) and request.FILES['file'] is not None:
            user = get_or_none(User, token=request.POST['token'])  # Validating token
            if user is None:
                return json_error("Error. Update token")

            file_entry = File.objects.create(file_id=get_unique_id(), file_name=request.POST['file_name'], user_id=user,
                                             size=0)

            abs_path = str(settings.FILES_FOLDER / file_entry.file_id)
            with open(abs_path, 'wb+') as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
            new_size = os.path.getsize(abs_path)
            file_entry.size = new_size
            file_entry.save()

            sum = File.objects.filter(user_id=user).aggregate(Sum('size'))
            if int(sum['size__sum']) > int(LIMIT_MEMORY):  # If more than 100 mb then cannot upload
                os.remove(abs_path)
                file_entry.delete()
                return json_error("Limit. You cannot upload files in sum more than 100mb")

            start_new_thread(archive_file, (file_entry.file_id,))

            response = {"file_id": file_entry.file_id}

            return JsonResponse(response, safe=False)

        return json_error("Request is invalid. Check that you sent file, token (less than 256), file_name (less "
                          "than 512) and not none")
    return json_error("API supports only GET and POST methods")


@csrf_exempt
def get_token(request: HttpRequest):
    if request.method == "GET":
        return json_error("Use method POST. username and password in plain text")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return json_error("Couldn't decode your json request")
        if validate_json(data, username=True, password=True):
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is None:
                return json_error("This user already exists")
            user.get_new_token()
            user.save()
            return JsonResponse({"token": user.token}, safe=False)
        return json_error("Wrong format")
    return json_error("API supports only GET and POST methods")


@csrf_exempt
def reg_view(request: HttpRequest):
    if request.method == "GET":
        return json_error("Use post method and specify your username and password")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return json_error("Couldn't decode your json request")
        if validate_json(data, username=True, password=True):
            user_exist = get_or_none(User, username=data['username'])
            if user_exist is not None:
                return json_error("Error. User with this username alerady exists")
            instance = User(username=data['username'])
            instance.get_new_token()
            instance.set_password(data['password'])
            instance.save()
            return JsonResponse({"token": instance.token}, safe=False)
        return json_error("Username (less that 150) and password (less than 50) should be not none")
    return json_error("Site supprots only GET and POST methods")


@csrf_exempt
def folder_content_view(request: HttpRequest):
    if request.method == "GET":
        return json_error("Use post method and specify your username and password")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return json_error("Couldn't decode your json request")
        if validate_json(data, token=True, file_id=True):
            user = get_or_none(User, token=data['token'])  # Validating token
            if user is None:
                return json_error("Error. Update token")

            if not has_access(user=user, file_id=data['file_id']):
                return json_error("You do not have accsess to this file/folder")

            fold = get_or_none(File, file_id=data['file_id'])
            if fold.is_folder is False:
                return json_error("This is file, not folder")

            files = []
            buff_list = list(File.objects.filter(parent=fold))
            for el in buff_list:
                if el.is_trash is True:
                    continue
                files.append({"file_id": el.file_id, "is_folder": el.is_folder, "name": el.file_name})

            return JsonResponse(files, safe=False)
        return json_error("Wrong credentials")
    return json_error("Site supprots only GET and POST methods")


@csrf_exempt
def grand_accsess_view(request: HttpRequest):
    if request.method == "GET":
        return json_error("Use post method and specify your username and password")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return json_error("Couldn't decode your json request")
        if validate_json(data, token=True, file_id=True, username=True):  # can_edit=True
            user = validate_user(data, check_owner=True)
            if str(type(user)) == "<class 'str'>":
                return json_error(str(user))

            share_uid = get_or_none(User, username=data['username'])
            if share_uid is None:
                return json_error("There is no such user")

            # can_edit = data['can_edit'] == 'True'
            Access(file_id=data['file_id'], owner_id=user, share_uid=share_uid, can_edit=True).save()
            return JsonResponse({"message": "successful"})
        return json_error("Wrong credentials")
    return json_error("Site supprots only GET and POST methods")


@csrf_exempt
def create_dir(request: HttpRequest):
    if request.method == "GET":
        return json_error("Use post method and specify your token, file_name (folder name)")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return json_error("Couldn't decode your json request")
        if validate_json(data, token=True, file_name=True):
            user = validate_user(data)
            if str(type(user)) == "<class 'str'>":
                return json_error(str(user))

            fold_file = File.objects.create(file_id=get_unique_id(), user_id=user, is_folder=True,
                                            file_name=data['file_name'], size=0)

            return JsonResponse({"file_id": fold_file.file_id})
        return json_error("Wrong credentials")
    return json_error("Site supprots only GET and POST methods")


@csrf_exempt
def move_file_to_dir(request: HttpRequest):
    if request.method == "GET":
        return json_error("Use post method and specify your token, file_id ans fold_id")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return json_error("Couldn't decode your json request")
        if validate_json(data, token=True, file_id=True, fold_id=True):
            user = validate_user(data, check_owner=True, check_owner_folder=True)
            if str(type(user)) == "<class 'str'>":
                return json_error(str(user))

            folder_entry = get_or_none(File, file_id=data['fold_id'])
            if folder_entry is None:
                return json_error("There os no such folder")
            if folder_entry.is_folder is False:
                return json_error(f"{data['fold_id']} is not a folder")

            file_entry = get_or_none(File, file_id=data['file_id'])
            if file_entry is None:
                return json_error("There os no such file")

            File.objects.filter(id=file_entry.id).update(parent=folder_entry)

            return JsonResponse({"message": "success"})
        return json_error("Wrong credentials")
    return json_error("Site supprots only GET and POST methods")


@csrf_exempt
def get_all_files_view(request: HttpRequest):
    if request.method == "GET":
        return json_error("Use post method and specify your token")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return json_error("Couldn't decode your json request")
        if validate_json(data, token=True):
            user = validate_user(data)
            if str(type(user)) == "<class 'str'>":
                return json_error(str(user))

            files = []
            buff_list = list(File.objects.filter(user_id=user))
            for el in buff_list:
                if el.is_trash is True:
                    continue
                if el.parent is None:
                    pr = 'root'
                else:
                    pr = el.parent.file_id
                files.append({"file_id": el.file_id, "is_folder": el.is_folder, "name": el.file_name, "parent": pr,
                              "date_of_creation": el.date_of_creation, "size": el.size})

            return JsonResponse(files, safe=False)
        return json_error("Wrong credentials")
    return json_error("Site supprots only GET and POST methods")


@csrf_exempt
def delete_view(request: HttpRequest):
    if request.method == "GET":
        return json_error("Use post method and specify your token and file_id")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return json_error("Couldn't decode your json request")
        if validate_json(data, token=True, file_id=True):
            user = validate_user(data)
            if str(type(user)) == "<class 'str'>":
                return json_error(str(user))

            if not has_access(user=user, file_id=data['file_id']):
                return json_error("You do not have accsess to this file/folder")

            file2del = get_or_none(File, file_id=data['file_id'])
            if file2del is None:
                return json_error("There is no such file")
            if file2del.is_trash is True:
                path = absolute_path_from_filename(file2del.file_id + ".7z")
                os.remove(path)
                file2del.delete()
                return JsonResponse({"message": "Deleted"})

            File.objects.filter(id=file2del.id).update(is_trash=True, trash_date=datetime.datetime.now())

            return JsonResponse({"message": "Moved to trash"})
        return json_error("Wrong credentials")
    return json_error("Site supprots only GET and POST methods")


# rename
@csrf_exempt
def rename_view(request: HttpRequest):
    if request.method == "GET":
        return json_error("Use post method and specify your token, file_id and new_name")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return json_error("Couldn't decode your json request")
        if validate_json(data, token=True, file_id=True, new_name=True):
            user = validate_user(data)
            if str(type(user)) == "<class 'str'>":
                return json_error(str(user))
            if not has_access(user=user, file_id=data['file_id']):
                return json_error("You do not have accsess to this file/folder")

            File.objects.filter(file_id=data['file_id']).update(file_name=data['new_name'])

            return JsonResponse({"message": "successful"})
        return json_error("Wrong credentials")
    return json_error("Site supprots only GET and POST methods")


# get space
@csrf_exempt
def get_space_view(request: HttpRequest):
    if request.method == "GET":
        return json_error("Use post method and specify your token")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return json_error("Couldn't decode your json request")
        if validate_json(data, token=True):
            user = validate_user(data)
            if str(type(user)) == "<class 'str'>":
                return json_error(str(user))

            sum = File.objects.filter(user_id=user).aggregate(Sum('size'))

            return JsonResponse({"size": str(sum['size__sum'])})
        return json_error("Wrong credentials")
    return json_error("Site supprots only GET and POST methods")


def main_validator(request, get_req, file_id=False, file_name=False, username=False, password=False, can_edit=False,
                   fold_id=False, new_name=False):
    if request.method == "GET":
        return json_error(f"Use post method and specify {get_req}")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            return json_error("Couldn't decode your json request")
        if not validate_json(data, token=True, file_id=file_id, file_name=file_name, username=username,
                             password=password, can_edit=can_edit, fold_id=fold_id, new_name=new_name):
            return json_error("Wrong credentials")
        return None
    return json_error("Site supprots only GET and POST methods")


@csrf_exempt
def clear_trash_bin_view(request: HttpRequest):
    result_of_valid = main_validator(request=request, get_req="token")
    if result_of_valid is not None:
        return result_of_valid
    data = json.loads(request.body.decode())
    user = validate_user(data)
    if str(type(user)) == "<class 'str'>":
        return json_error(str(user))

    files2delete = list(File.objects.filter(is_trash=True, user_id=user))
    for el in files2delete:
        path = absolute_path_from_filename(el.file_id + ".7z")
        os.remove(path)
        el.delete()

    return JsonResponse({"message": "successfuly cleaned trash"})


@csrf_exempt
def get_all_in_trash(request: HttpRequest):
    result_of_valid = main_validator(request=request, get_req="token")
    if result_of_valid is not None:
        return result_of_valid
    data = json.loads(request.body.decode())
    user = validate_user(data)
    if str(type(user)) == "<class 'str'>":
        return json_error(str(user))

    files = []
    buff_list = list(File.objects.filter(user_id=user, is_trash=True))
    for el in buff_list:
        if el.parent is None:
            pr = 'root'
        else:
            pr = el.parent.file_id
        files.append({"file_id": el.file_id, "is_folder": el.is_folder, "name": el.file_name, "parent": pr,
                      "date_of_creation": el.date_of_creation, "size": el.size})
    return JsonResponse(files, safe=False)


@csrf_exempt
def get_all_users_view(request: HttpRequest):
    result_of_valid = main_validator(request=request, get_req="token")
    if result_of_valid is not None:
        return result_of_valid
    data = json.loads(request.body.decode())
    user = validate_user(data)
    if str(type(user)) == "<class 'str'>":
        return json_error(str(user))

    if user.is_superuser is False:
        return json_error("You are not admin. So not allowed to see this page")

    users = []
    buff_list = list(User.objects.all())
    for el in buff_list:
        users.append({"username": el.username})
    return JsonResponse(users, safe=False)


@csrf_exempt
def get_all_files_of_user_view(request: HttpRequest):
    result_of_valid = main_validator(request=request, get_req="token", username=True)
    if result_of_valid is not None:
        return result_of_valid
    data = json.loads(request.body.decode())
    user = validate_user(data)
    if str(type(user)) == "<class 'str'>":
        return json_error(str(user))

    if user.is_superuser is False:
        return json_error("You are not admin. So not allowed to see this page")

    user_to_see = get_or_none(User, username=data['username'])
    if user_to_see is None:
        return json_error("No such user")

    files = []
    buff_list = list(File.objects.filter(user_id=user_to_see))
    for el in buff_list:
        files.append({"file_name": el.file_name})
    return JsonResponse(files, safe=False)
