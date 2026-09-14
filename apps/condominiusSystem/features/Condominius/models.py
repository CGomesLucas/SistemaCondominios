from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

class TypeCondominius(models.TextChoices):  
    RESIDENCIAL = 'Residencial'
    COMERCIAL = 'Comercial'
    MISTO = 'Misto'

class Condominius(models.Model):

    name = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=18, validators=[MinLengthValidator(18)])
    type_condominious = models.CharField(choices=TypeCondominius.choices)
    quantity_building = models.IntegerField(validators=[MinValueValidator(1)])
    cep = models.CharField(max_length=8, validators=[MinLengthValidator(8)])
    logradouro = models.CharField(max_length=150)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2, validators=[MinLengthValidator(2)])

    class Meta:
        app_label = "condominiusSystem"
