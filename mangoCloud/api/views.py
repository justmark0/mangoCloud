from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, render
from django.http import HttpRequest, FileResponse
from .models import File
from .services import *
from .forms import *
import json


@csrf_exempt
def get_file(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse("Specify files that you need to receive, and your token. Communicate with POST method")
    if request.method == "POST":
        form = GetFile(request.POST)
        if form.is_valid():
            # TODO check if token is correct
            # Get file from folder and send to client    form.cleaned_data['token']
            file = absolute_path_from_filename(form.cleaned_data['file_id'])
            file_entry = get_or_none(File, file_id=form.cleaned_data['file_id'])
            if file_entry is None or file is None:
                return HttpResponse("There is no such file")
            return FileResponse(open(file, 'rb'), filename=file_entry.file_name)
        return HttpResponse("Error. Check if file name (less 512) and token is less than 256 symbols and not none")
    return HttpResponse("API supprots only GET and POST methods")


@csrf_exempt
def upload_file(request: HttpRequest):
    if request.method == "GET":
        return render(request, 'index.html', {'form': UploadFile()})
        # return HttpResponse("Use method POST. token (max symbols 512) and file")
    if request.method == "POST":
        form = UploadFile(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            # user = get_or_none(User, token=form.cleaned_data['token']) # TODO check users token
            # if user is None:
            #     return HttpResponse("Error. Update token")
            file_entry = File.objects.create(file_id=create_file_id(), file_name=form.cleaned_data['file'])
            save_file_in_folder(name=file_entry.file_id, file=request.FILES['file'])
            response = {"file_id": file_entry.file_id}
            return HttpResponse(json.dumps(response))
        return HttpResponse("Request is invalid. Check that you sent file, token (less than 256), file_name (less "
                            "than 512) and not none")
    return HttpResponse("API supports only GET and POST methods")


@csrf_exempt
def get_token(request: HttpRequest):
    pass