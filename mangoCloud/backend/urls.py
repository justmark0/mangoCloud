from django.urls import path
from .views import *

urlpatterns = [
    path('', index_view),
    path('login', login_view),
    path('registrate', reg_view),
]
