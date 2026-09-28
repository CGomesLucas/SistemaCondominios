from decimal import Decimal

from django.db import models

from apps.condominiusSystem.features.Charge.models import Charge
from apps.condominiusSystem.features.Unity.models import Unity


class AgreementStatus(models.TextChoices):
    ATIVO = "ATIVO", "Ativo"
    QUITADO = "QUITADO", "Quitado"
    CANCELADO = "CANCELADO", "Cancelado"


class InstallmentStatus(models.TextChoices):
    PENDENTE = "PENDENTE", "Pendente"
    PAGO = "PAGO", "Pago"


class Agreement(models.Model):
    unidade = models.ForeignKey(Unity, on_delete=models.CASCADE, related_name="acordos")
    cobrancas = models.ManyToManyField(Charge, related_name="acordos")
    quantidade_parcelas = models.PositiveSmallIntegerField()
    data_primeira_parcela = models.DateField()
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(
        max_length=10,
        choices=AgreementStatus.choices,
        default=AgreementStatus.ATIVO,
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "condominiusSystem"
        ordering = ["-criado_em"]
        verbose_name = "Acordo"
        verbose_name_plural = "Acordos"

    def __str__(self):
        return f"Acordo {self.pk} - {self.unidade}"


class AgreementInstallment(models.Model):
    acordo = models.ForeignKey(Agreement, on_delete=models.CASCADE, related_name="parcelas")
    numero = models.PositiveSmallIntegerField()
    data_vencimento = models.DateField()
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=InstallmentStatus.choices,
        default=InstallmentStatus.PENDENTE,
    )
    data_pagamento = models.DateField(null=True, blank=True)

    class Meta:
        app_label = "condominiusSystem"
        ordering = ["acordo", "numero"]
        constraints = [
            models.UniqueConstraint(
                fields=["acordo", "numero"],
                name="unique_installment_number_per_agreement",
            )
        ]
        verbose_name = "Parcela do acordo"
        verbose_name_plural = "Parcelas do acordo"

    def __str__(self):
        return f"Parcela {self.numero} do acordo {self.acordo_id}"