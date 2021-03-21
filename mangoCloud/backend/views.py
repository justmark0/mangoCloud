from django.shortcuts import render, HttpResponse, redirect
# from django.contrib.auth import authenticate, login
# from .forms import UserForm, LoginForm
from django.http import HttpRequest, FileResponse, JsonResponse
from api.models import File
from api.services import has_access, delete_file_after_5s, absolute_path_from_filename
from _thread import start_new_thread
from .models import User
from django.http import HttpRequest
import py7zr
# from .models import User


def json_error(message):
    return JsonResponse({"Error": message}, safe=False)


def json_message(message):
    return JsonResponse({"message": message}, safe=False)


def get_or_none(classname, **kwargs):
    try:
        return classname.objects.get(**kwargs)
    except classname.DoesNotExist:
        return None


def index_view(request: HttpRequest):
    return render(request, 'index.html')


def file_view(request: HttpRequest, file_id):
    if request.method == "GET":
        if not 'token' in request.COOKIES.keys():
            return json_error("Error. Update token")
        user = get_or_none(User, token=request.COOKIES['token'])
        if user is None:
            return json_error("Error. Update token")
        if not has_access(user, file_id):
            return json_error("You have no rights to see this file")
        file_entry = get_or_none(File, file_id=file_id)
        if file_entry is None:
            return json_error("There is no such file")

        file = absolute_path_from_filename(file_id + ".7z")
        archive = py7zr.SevenZipFile(file, mode='r')
        archive.extractall(path=file[:-3:])
        archive.close()
        start_new_thread(delete_file_after_5s, (file[:-3:],))

        return FileResponse(open(str(file[:-3:] + "/" + file_entry.file_id), 'rb'), filename=file_entry.file_name)

#
#
# def login_view(request: HttpRequest):
#     if request.method == "GET":
#         return render(request, 'login.html', {"form": UserForm()})
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         print(form.errors)
#         if form.is_valid():
#             user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
#             if user is not None:
#                 login(request, user)
#                 return redirect('/', {"message": "Login successfully"})
#             else:
#                 return redirect('/', {"message": "No such user :("})
#         return HttpResponse("Username (less that 150) and password (less than 50) should be not none")
#     return HttpResponse("Site supprots only GET and POST methods")
#
#
# def reg_view(request: HttpRequest):
#     if request.method == "GET":
#         return render(request, 'reg.html', {"form": UserForm()})
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         print(form.errors)
#         print(request.body)
#         if form.is_valid():
#             instance = form.instance
#             print(instance)
#
#             instance.get_new_token()
#             instance.set_password(instance.password)
#             instance.save()
#             # user = authenticate(request, username=instance.username, password=instance.password)
#             # login(request, user)
#             return redirect('/', {"message": "You registrated successfully"})
#         if str(form.errors).find("User with this Username already exists."):
#             return HttpResponse("User with this Username already exists.")
#         return HttpResponse("Username (less that 150) and password (less than 50) should be not none")
#     return HttpResponse("Site supprots only GET and POST methods")
