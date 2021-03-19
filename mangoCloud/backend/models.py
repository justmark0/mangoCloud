from django.contrib.auth.models import AbstractUser
from api.services import get_unique_id  # It is right import
from django.db import models


class User(AbstractUser):
    token = models.CharField(max_length=256)
    username = models.CharField(max_length=150, unique=True)

    def get_new_token(self):
        self.token = get_unique_id(User)
        return self.token

    class Meta:
        indexes = [
            models.Index(fields=['username']),
        ]
