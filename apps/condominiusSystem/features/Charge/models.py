from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.condominiusSystem.features.Unity.models import Unity


class ChargeStatus(models.TextChoices):
    PENDENTE = "PENDENTE", "Pendente"
    PAGO = "PAGO", "Pago"
    VENCIDO = "VENCIDO", "Vencido"
    CANCELADO = "CANCELADO", "Cancelado"


class PaymentMethod(models.TextChoices):
    BOLETO = "BOLETO", "Boleto"
    PIX = "PIX", "Pix"
    CARTAO = "CARTAO", "Cartão"


class ChargeQuerySet(models.QuerySet):
    def refresh_overdue(self):
        return self.filter(
            status=ChargeStatus.PENDENTE,
            data_vencimento__lt=timezone.localdate(),
        ).update(status=ChargeStatus.VENCIDO)


class Charge(models.Model):
    unidade = models.ForeignKey(Unity, on_delete=models.CASCADE, related_name="cobrancas")
    competencia = models.DateField()
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_vencimento = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=ChargeStatus.choices,
        default=ChargeStatus.PENDENTE,
    )
    data_pagamento = models.DateField(null=True, blank=True)
    forma_pagamento = models.CharField(max_length=10, choices=PaymentMethod.choices, blank=True)
    multa = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    juros = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    objects = ChargeQuerySet.as_manager()

    class Meta:
        app_label = "condominiusSystem"
        ordering = ["-competencia", "unidade"]
        constraints = [
            models.UniqueConstraint(
                fields=["unidade", "competencia"],
                name="unique_charge_per_unit_competence",
            )
        ]
        verbose_name = "Cobrança"
        verbose_name_plural = "Cobranças"

    def save(self, *args, **kwargs):
        if self.status == ChargeStatus.PAGO:
            if not self.data_pagamento:
                raise ValidationError({"data_pagamento": "Informe a data do pagamento."})
            if not self.forma_pagamento:
                raise ValidationError({"forma_pagamento": "Informe a forma de pagamento."})
            self.calculate_late_charges(self.data_pagamento)
        elif self.status in (ChargeStatus.PENDENTE, ChargeStatus.VENCIDO):
            self.status = (
                ChargeStatus.VENCIDO
                if self.data_vencimento < timezone.localdate()
                else ChargeStatus.PENDENTE
            )
            self.data_pagamento = None
            self.forma_pagamento = ""
            self.multa = Decimal("0.00")
            self.juros = Decimal("0.00")
        super().save(*args, **kwargs)

    def calculate_late_charges(self, payment_date):
        days_late = max((payment_date - self.data_vencimento).days, 0)
        if days_late:
            self.multa = (self.valor * Decimal("0.02")).quantize(Decimal("0.01"))
            self.juros = (
                self.valor * Decimal("0.00033") * days_late
            ).quantize(Decimal("0.01"))
        else:
            self.multa = Decimal("0.00")
            self.juros = Decimal("0.00")

    def amount_due(self, on_date=None):
        on_date = on_date or timezone.localdate()
        days_late = max((on_date - self.data_vencimento).days, 0)
        if self.status == ChargeStatus.PAGO:
            return self.valor + self.multa + self.juros
        if not days_late:
            return self.valor
        fine = (self.valor * Decimal("0.02")).quantize(Decimal("0.01"))
        interest = (self.valor * Decimal("0.00033") * days_late).quantize(Decimal("0.01"))
        return self.valor + fine + interest

    def __str__(self):
        return f"{self.unidade} - {self.competencia:%m/%Y}"