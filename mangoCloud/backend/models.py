from django.contrib.auth.models import AbstractUser
from django.db import models
from random import randint
from hashlib import sha256


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


def get_or_none(classname, **kwargs):
    try:
        return classname.objects.get(**kwargs)
    except classname.DoesNotExist:
        return None


def get_unique_id(classname):
    while True:
        a = str(randint(0, int(1e9))) + str(randint(0, int(1e9)))
        h = sha256(a.encode()).hexdigest()
        entry = get_or_none(classname, token=h)
        if entry is None:
            return h
