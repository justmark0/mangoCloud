from django.urls import path
from .views import *

urlpatterns = [
    path('get_file', get_file),
    path('upload_file', upload_file),
    path('get_token', get_token),
    path('reg', reg_view),
]
