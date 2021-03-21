from _thread import start_new_thread
from .services import clean_trash
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
    path('get_all_files', get_all_files_view),
    path('delete', delete_view),
    path('rename', rename_view),
    path('using_space', get_space_view),
    path('get_all_in_trash', get_all_in_trash),
    path('get_all_users', get_all_users_view),
    path('get_all_files_of_user', get_all_files_of_user_view),
]

start_new_thread(clean_trash, ())
