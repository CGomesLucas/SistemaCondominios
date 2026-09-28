from rest_framework import serializers

from apps.condominiusSystem.features.Condominius.models import Condominius

from .models import Unity


class UnitySerializer(serializers.ModelSerializer):
    building = serializers.CharField(required=False, allow_blank=True)
    condominio_id = serializers.PrimaryKeyRelatedField(
        source="condominio",
        queryset=Condominius.objects.all(),
    )

    class Meta:
        model = Unity
        fields = [
            "id",
            "number",
            "building",
            "responsible_name",
            "status",
            "is_active",
            "condominio_id",
        ]
        read_only_fields = ["id"]
        validators = []

    def validate(self, attrs):
        instance = self.instance
        condominio = attrs.get("condominio", getattr(instance, "condominio", None))
        building = attrs.get("building", getattr(instance, "building", ""))
        number = attrs.get("number", getattr(instance, "number", None))
        duplicates = Unity.objects.filter(
            condominio=condominio,
            building=building,
            number=number,
        )
        if instance:
            duplicates = duplicates.exclude(pk=instance.pk)
        if duplicates.exists():
            raise serializers.ValidationError("Já existe uma unidade com esse bloco e número no condomínio.")
        return attrs
        