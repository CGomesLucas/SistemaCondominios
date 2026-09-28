from django.db import models


class TypeCondominius(models.TextChoices):
    RESIDENCIAL = "RESIDENCIAL", "Residencial"
    COMERCIAL = "COMERCIAL", "Comercial"
    MISTO = "MISTO", "Misto"


class Condominius(models.Model):
    name = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=18, blank=True)
    type_condominious = models.CharField(
        max_length=20,
        choices=TypeCondominius.choices,
        default=TypeCondominius.RESIDENCIAL,
    )
    quantity_building = models.PositiveIntegerField(default=1)
    cep = models.CharField(max_length=9, blank=True)
    logradouro = models.CharField(max_length=150, blank=True)
    numero = models.CharField(max_length=20, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    uf = models.CharField(max_length=2, blank=True)

    class Meta:
        app_label = "condominiusSystem"
        ordering = ["name"]
        verbose_name = "Condomínio"
        verbose_name_plural = "Condomínios"

    def __str__(self):
        return self.name
