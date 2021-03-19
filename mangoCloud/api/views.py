from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, render
from django.http import HttpRequest, FileResponse
from backend.models import User  # It is right import
from django.contrib.auth import authenticate
from .models import File
from .services import *
from .forms import *
import json


@csrf_exempt
def get_file(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse("Specify files that you need to receive, and your token. Communicate with POST method")
    if request.method == "POST":
        data = json.loads(request.body.decode())
        if validate_json(data, token=True, file_id=True):
            user = get_or_none(User, token=data['token'])  # Validating token
            if user is None:
                return HttpResponse("Error. Update token")

            file = absolute_path_from_filename(data['file_id'])
            file_entry = get_or_none(File, file_id=data['file_id'])
            if file_entry is None or file is None:
                return HttpResponse("There is no such file")

            if file_entry.user_id != user.user_id:
                return HttpResponse("You have no rights to see this file")

            return FileResponse(open(file, 'rb'), filename=file_entry.file_name)
        return HttpResponse("Error. Check if file name (less 512) and token is less than 256 symbols and not none")
    return HttpResponse("API supprots only GET and POST methods")


@csrf_exempt
def upload_file(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse("Use method POST. token (max symbols 512) and file")
    if request.method == "POST":
        data = json.loads(request.body.decode())
        if validate_json(data, token=True, file_name=True) and request.FILES['file']:
            user = get_or_none(User, token=data['token'])  # Validating token
            if user is None:
                return HttpResponse("Error. Update token")

            file_entry = File.objects.create(file_id=get_unique_id(), file_name=data['file_name'], user_id=user.user_id)
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
        data = json.loads(request.body.decode())
        if validate_json(data, username=True, password=True):
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is None:
                return HttpResponse("Wrong username or password")
            user.get_new_token()
            user.save()
            return HttpResponse(json.dumps({"token": user.token}))
        return HttpResponse("Wrong format")
    return HttpResponse("API supports only GET and POST methods")


@csrf_exempt
def reg_view(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse("Use post method and specify your username and password")
    if request.method == "POST":
        data = json.loads(request.body.decode())
        if validate_json(data, username=True, password=True):
            user_exist = get_or_none(User, username=data['username'])
            if user_exist is not None:
                return HttpResponse("Error. User with this username alerady exists")
            instance = User(username=data['username'])
            instance.get_new_token()
            instance.set_password(data['password'])
            instance.save()
            return HttpResponse(json.dumps({"token": instance.token}))
        return HttpResponse("Username (less that 150) and password (less than 50) should be not none")
    return HttpResponse("Site supprots only GET and POST methods")
