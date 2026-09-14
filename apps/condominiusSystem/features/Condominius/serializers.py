from rest_framework import serializers
from .models import Condominius


class CondominiusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condominius
        fields = "__all__"