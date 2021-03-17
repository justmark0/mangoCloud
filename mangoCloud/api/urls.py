from django.urls import path
from .views import *

urlpatterns = [
    path('getfile/', get_file),
    path('uploadfile/', upload_file),
    path('gettoken/', get_token),
]
