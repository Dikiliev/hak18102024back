from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Админ'
        PRORECTOR = 'prorector', 'Проректор'
        REVIEWER = 'reviewer', 'Проверяющий'
        STUDENT = 'student', 'Студент'

    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.STUDENT
    )

    signature = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username
