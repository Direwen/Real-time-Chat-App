from django.db import models
from django.contrib.auth.models import AbstractUser

#Don't Forget to import the modified user model in settings
class User(AbstractUser):
    email = models.EmailField(unique=True)