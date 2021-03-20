from django.urls import path
from .views import *

urlpatterns = [
    path('', index_view),
    path('file/<file_id>', file_view)
    # path('login', login_view),
    # path('registrate', reg_view),
]
