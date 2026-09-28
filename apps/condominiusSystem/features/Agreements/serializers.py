import calendar
from datetime import date
from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from apps.condominiusSystem.features.Charge.models import Charge, ChargeStatus
from apps.condominiusSystem.features.Unity.models import Unity

from .models import (
    Agreement,
    AgreementInstallment,
    AgreementStatus,
    InstallmentStatus,
)


class AgreementInstallmentSerializer(serializers.ModelSerializer):
    acordo_id = serializers.PrimaryKeyRelatedField(
        source="acordo",
        read_only=True,
    )

    class Meta:
        model = AgreementInstallment
        fields = ["id", "acordo_id", "numero", "data_vencimento", "valor", "status", "data_pagamento"]
        read_only_fields = ["id", "numero", "data_vencimento", "valor"]

    def validate(self, attrs):
        instance = self.instance
        status = attrs.get("status", getattr(instance, "status", InstallmentStatus.PENDENTE))
        payment_date = attrs.get("data_pagamento", getattr(instance, "data_pagamento", None))
        if instance and instance.acordo.status == AgreementStatus.CANCELADO:
            raise serializers.ValidationError(
                {"acordo_id": "Não é possível alterar parcelas de um acordo cancelado."}
            )
        if status == InstallmentStatus.PAGO:
            if not payment_date:
                raise serializers.ValidationError({"data_pagamento": "Informe a data do pagamento."})
            if payment_date > timezone.localdate():
                raise serializers.ValidationError({"data_pagamento": "A data não pode estar no futuro."})
        elif payment_date is not None:
            raise serializers.ValidationError(
                {"data_pagamento": "Limpe a data de pagamento para manter a parcela pendente."}
            )
        return attrs

    def _update_agreement_status(self, installment):
        agreement = installment.acordo
        if agreement.status == AgreementStatus.CANCELADO:
            return
        all_paid = not agreement.parcelas.exclude(status=InstallmentStatus.PAGO).exists()
        agreement.status = AgreementStatus.QUITADO if all_paid else AgreementStatus.ATIVO
        agreement.save(update_fields=["status"])

    def create(self, validated_data):
        installment = super().create(validated_data)
        self._update_agreement_status(installment)
        return installment

    def update(self, instance, validated_data):
        installment = super().update(instance, validated_data)
        self._update_agreement_status(installment)
        return installment


class AgreementSerializer(serializers.ModelSerializer):
    unidade_id = serializers.PrimaryKeyRelatedField(source="unidade", queryset=Unity.objects.all())
    cobrancas_ids = serializers.PrimaryKeyRelatedField(
        source="cobrancas",
        many=True,
        queryset=Charge.objects.all(),
    )
    parcelas = AgreementInstallmentSerializer(many=True, read_only=True)

    class Meta:
        model = Agreement
        fields = [
            "id",
            "unidade_id",
            "cobrancas_ids",
            "quantidade_parcelas",
            "data_primeira_parcela",
            "valor_total",
            "status",
            "criado_em",
            "parcelas",
        ]
        read_only_fields = ["id", "valor_total", "criado_em", "parcelas"]

    def validate(self, attrs):
        today = timezone.localdate()
        Charge.objects.refresh_overdue()
        instance = self.instance
        unidade = attrs.get("unidade", getattr(instance, "unidade", None))
        cobrancas = attrs.get(
            "cobrancas",
            list(instance.cobrancas.all()) if instance else [],
        )
        quantidade = attrs.get("quantidade_parcelas", getattr(instance, "quantidade_parcelas", 0))
        primeira_data = attrs.get(
            "data_primeira_parcela",
            getattr(instance, "data_primeira_parcela", None),
        )

        if not cobrancas:
            raise serializers.ValidationError({"cobrancas_ids": "Selecione ao menos uma cobrança."})
        if len({charge.pk for charge in cobrancas}) != len(cobrancas):
            raise serializers.ValidationError(
                {"cobrancas_ids": "Não informe a mesma cobrança mais de uma vez."}
            )
        if not 1 <= quantidade <= 48:
            raise serializers.ValidationError({"quantidade_parcelas": "Use entre 1 e 48 parcelas."})
        if not instance and primeira_data < today:
            raise serializers.ValidationError({"data_primeira_parcela": "A primeira parcela não pode vencer no passado."})
        if instance and instance.status == AgreementStatus.CANCELADO:
            schedule_changed = (
                unidade.pk != instance.unidade_id
                or quantidade != instance.quantidade_parcelas
                or primeira_data != instance.data_primeira_parcela
                or {item.pk for item in cobrancas} != set(instance.cobrancas.values_list("pk", flat=True))
            )
            if schedule_changed:
                raise serializers.ValidationError(
                    {"status": "Não é possível alterar um acordo cancelado."}
                )

        for charge in cobrancas:
            charge.refresh_from_db(fields=["status", "data_vencimento"])
            if charge.unidade_id != unidade.pk:
                raise serializers.ValidationError({"cobrancas_ids": "Todas as cobranças devem pertencer à mesma unidade."})
            if charge.status != ChargeStatus.VENCIDO or charge.data_vencimento >= today:
                raise serializers.ValidationError({"cobrancas_ids": "O acordo só pode incluir cobranças vencidas e em aberto."})
            active_agreements = charge.acordos.filter(status=AgreementStatus.ATIVO)
            if instance:
                active_agreements = active_agreements.exclude(pk=instance.pk)
            if active_agreements.exists():
                raise serializers.ValidationError({"cobrancas_ids": "Uma cobrança já está em outro acordo ativo."})

        if instance and instance.parcelas.filter(status=InstallmentStatus.PAGO).exists():
            schedule_changed = (
                unidade.pk != instance.unidade_id
                or quantidade != instance.quantidade_parcelas
                or primeira_data != instance.data_primeira_parcela
                or {item.pk for item in cobrancas} != set(instance.cobrancas.values_list("pk", flat=True))
            )
            if schedule_changed:
                raise serializers.ValidationError("Não é possível alterar o cronograma após o pagamento de uma parcela.")
        attrs["cobrancas"] = cobrancas
        return attrs

    def validate_status(self, value):
        if self.instance is None:
            if value != AgreementStatus.ATIVO:
                raise serializers.ValidationError(
                    "Um acordo novo começa ativo; o status quitado é definido pelo pagamento das parcelas."
                )
            return value

        if value == self.instance.status:
            return value
        if self.instance.status == AgreementStatus.ATIVO and value == AgreementStatus.CANCELADO:
            return value
        raise serializers.ValidationError(
            "O status quitado é definido pelo pagamento das parcelas; somente acordos ativos podem ser cancelados."
        )

    @staticmethod
    def _add_months(start_date: date, months: int) -> date:
        month_index = start_date.year * 12 + start_date.month - 1 + months
        year, month_index = divmod(month_index, 12)
        month = month_index + 1
        day = min(start_date.day, calendar.monthrange(year, month)[1])
        return date(year, month, day)

    def _generate_installments(self, agreement, cobrancas):
        today = timezone.localdate()
        total = sum((charge.amount_due(today) for charge in cobrancas), Decimal("0.00"))
        agreement.valor_total = total.quantize(Decimal("0.01"))
        agreement.save()
        agreement.cobrancas.set(cobrancas)
        agreement.parcelas.all().delete()

        regular_value = (agreement.valor_total / agreement.quantidade_parcelas).quantize(Decimal("0.01"))
        remaining = agreement.valor_total
        for number in range(1, agreement.quantidade_parcelas + 1):
            value = remaining if number == agreement.quantidade_parcelas else regular_value
            AgreementInstallment.objects.create(
                acordo=agreement,
                numero=number,
                data_vencimento=self._add_months(agreement.data_primeira_parcela, number - 1),
                valor=value,
            )
            remaining -= value

    @transaction.atomic
    def create(self, validated_data):
        cobrancas = validated_data.pop("cobrancas")
        agreement = Agreement.objects.create(**validated_data)
        self._generate_installments(agreement, cobrancas)
        return agreement

    @transaction.atomic
    def update(self, instance, validated_data):
        cobrancas = validated_data.pop("cobrancas", list(instance.cobrancas.all()))
        schedule_changed = (
            validated_data.get("unidade", instance.unidade).pk != instance.unidade_id
            or validated_data.get("quantidade_parcelas", instance.quantidade_parcelas) != instance.quantidade_parcelas
            or validated_data.get("data_primeira_parcela", instance.data_primeira_parcela) != instance.data_primeira_parcela
            or {item.pk for item in cobrancas} != set(instance.cobrancas.values_list("pk", flat=True))
        )
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        if schedule_changed:
            self._generate_installments(instance, cobrancas)
        return instance