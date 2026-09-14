from django.core.validators import MinLengthValidator, MinValueValidator
from features.Condominius.models import Condominius
from django.db import models

class StatusUnity(models.TextChoices):  
    OCUPADO = 'Ocupado'
    VAGO = 'Vago'

class Unity(models.Model):

    number = models.CharField(max_length=20)
    building = models.CharField(max_length=20)
    status = models.CharField(choices=StatusUnity.choices)
    is_active = models.BooleanField(default=True)

    condominius = models.ForeignKey(
    Condominius,
    on_delete=models.CASCADE
    )

    class Meta:
        app_label = "condominiusSystem"