from apps.condominiusSystem.features.Condominius.models import Condominius
from django.db import models
from django.db.models import Q


class StatusUnity(models.TextChoices):
    OCUPADO = "OCUPADO", "Ocupado"
    VAGO = "VAGO", "Vago"


class Unity(models.Model):
    number = models.CharField(max_length=20)
    building = models.CharField(max_length=20, blank=True)
    responsible_name = models.CharField(max_length=150, blank=True)
    status = models.CharField(
        max_length=10,
        choices=StatusUnity.choices,
        default=StatusUnity.VAGO,
    )
    is_active = models.BooleanField(default=True)
    condominio = models.ForeignKey(
        Condominius,
        on_delete=models.CASCADE,
        related_name="unidades",
    )

    class Meta:
        app_label = "condominiusSystem"
        ordering = ["condominio", "building", "number"]
        constraints = [
            models.UniqueConstraint(
                fields=["condominio", "number"],
                condition=Q(building=""),
                name="unique_unit_no_block",
            ),
            models.UniqueConstraint(
                fields=["condominio", "building", "number"],
                condition=~Q(building=""),
                name="unique_unit_in_block",
            ),
        ]
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"

    def __str__(self):
        label = f"{self.building} - " if self.building else ""
        return f"{label}{self.number} ({self.condominio})"