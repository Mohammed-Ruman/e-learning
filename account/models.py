from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from .manager import UserManager

class CustomUser(AbstractUser):
    username = None
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_teacher = models.BooleanField(default=False)
    password = models.CharField(max_length=8)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, default="000000")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

