from django.shortcuts import render, HttpResponse


def index_view(request):
    return render(request, 'index.html')
