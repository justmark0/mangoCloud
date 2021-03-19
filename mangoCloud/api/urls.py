from django.urls import path
from .views import *

urlpatterns = [
    path('get_file', get_file),
    path('upload_file', upload_file),
    path('get_token', get_token),
    path('reg', reg_view),
    path('folder_content', folder_content_view),
    path('give_accsess', grand_accsess_view),
    path('mkdir', create_dir),
    path('mv_file2dir', move_file_to_dir),
]
