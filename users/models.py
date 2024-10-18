from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return self.username
