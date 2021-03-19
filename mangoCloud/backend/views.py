from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm, LoginForm
from django.http import HttpRequest
from .models import User


def index_view(request: HttpRequest):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def login_view(request: HttpRequest):
    if request.method == "GET":
        return render(request, 'login.html', {"form": UserForm()})
    if request.method == "POST":
        form = LoginForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/', {"message": "Login successfully"})
            else:
                return redirect('/', {"message": "No such user :("})
        return HttpResponse("Username (less that 150) and password (less than 50) should be not none")
    return HttpResponse("Site supprots only GET and POST methods")


def reg_view(request: HttpRequest):
    if request.method == "GET":
        return render(request, 'reg.html', {"form": UserForm()})
    if request.method == "POST":
        form = UserForm(request.POST)
        print(form.errors)
        if form.is_valid():
            instance = form.instance
            instance.get_new_token()
            instance.set_password(instance.password)
            instance.save()
            # user = authenticate(request, username=instance.username, password=instance.password)
            # login(request, user)
            return redirect('/', {"message": "You registrated successfully"})
        if str(form.errors).find("User with this Username already exists."):
            return HttpResponse("User with this Username already exists.")
        return HttpResponse("Username (less that 150) and password (less than 50) should be not none")
    return HttpResponse("Site supprots only GET and POST methods")
