from django.utils import timezone
from rest_framework import serializers

from apps.condominiusSystem.features.Unity.models import Unity

from .models import Charge, ChargeStatus


class ChargeSerializer(serializers.ModelSerializer):
    unidade_id = serializers.PrimaryKeyRelatedField(
        source="unidade",
        queryset=Unity.objects.all(),
    )

    class Meta:
        model = Charge
        fields = [
            "id",
            "unidade_id",
            "competencia",
            "valor",
            "data_vencimento",
            "status",
            "data_pagamento",
            "forma_pagamento",
            "multa",
            "juros",
        ]
        read_only_fields = ["id", "multa", "juros"]

    def validate(self, attrs):
        instance = self.instance
        status = attrs.get("status", getattr(instance, "status", ChargeStatus.PENDENTE))
        payment_date = attrs.get("data_pagamento", getattr(instance, "data_pagamento", None))
        payment_method = attrs.get("forma_pagamento", getattr(instance, "forma_pagamento", ""))

        if status == ChargeStatus.PAGO:
            if not payment_date:
                raise serializers.ValidationError({"data_pagamento": "Informe a data do pagamento."})
            if not payment_method:
                raise serializers.ValidationError({"forma_pagamento": "Informe a forma de pagamento."})
            if payment_date > timezone.localdate():
                raise serializers.ValidationError({"data_pagamento": "A data não pode estar no futuro."})
        return attrs