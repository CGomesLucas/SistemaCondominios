from rest_framework import serializers
from .models import Unity, Condominius

class CondominiusResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condominius
        fields = ['id', 'name']

class UnitySerializer(serializers.ModelSerializer):

    condiminius = CondominiusResponseSerializer(read_only=True)

    class Meta:     
        model = Unity
        fields = "__all__"
        read_only_fields = ['id', 'is_active', 'condiminius'] 
        