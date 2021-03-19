from django.forms import ModelForm
from django import forms
from .models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", 'password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=50)
