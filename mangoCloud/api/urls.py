from django.urls import path
from .views import *

urlpatterns = [
    path('getfile/', get_file),
]
