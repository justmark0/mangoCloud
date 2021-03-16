from .services import absolute_path_from_filename, get_or_none
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, FileResponse
from django.shortcuts import HttpResponse
from .forms import GetFile
from .models import File


@csrf_exempt
def get_file(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse("Specify files that you need to receive, and your token. Communicate with POST method")
    if request.method == "POST":
        form = GetFile(request.POST)
        print(form.errors)
        print(form.cleaned_data)
        # print(form.file_id)

        if form.is_valid():
            # TODO check if token is correct
            # Get file from folder and send to client    form.cleaned_data['token']
            file = absolute_path_from_filename(form.cleaned_data['file_id'])
            file_entry = get_or_none(File, file_id=form.cleaned_data['file_id'])
            if file_entry is None or file is None:
                return HttpResponse("There is no such file")
            return FileResponse(open(file, 'rb'), filename=file_entry.file_name)
        return HttpResponse("Error. Check if file name or token is less than 512 symbols and not none")
