from django.core.validators import MinLengthValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.TextChoices):  
    ADMIN = 'Admin'
    CLIENT = 'Client'

class User(AbstractUser):

    role = models.CharField(choices=Role.choices, max_length=20, default= Role.CLIENT)

    class Meta:
        app_label = "condominiusSystem"
