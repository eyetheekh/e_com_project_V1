from django.db import models
from django.contrib.auth.models import AbstractUser


class customUser(AbstractUser):
    username = models.CharField(unique=True, max_length=30, null=False)
    email = models.EmailField()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
