from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Unity, Condominius
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from models import Unity, Condominius
from .serializers import UnitySerializer, CondominiusResponseSerializer

class UnityViewset (viewsets.ModelViewSet):
    serializer_class = UnitySerializer

    def get_queryset(self):
        condominius_id = self.kwargs.get('condominius_pk')
        
        return Unity.objects.filter(condominius_id=condominius_id, active=True)

    def perform_create(self, serializer):
        condominius_id = self.kwargs.get('condominius_pk')
        Condominius = get_object_or_404(Condominius, pk=id)
        serializer.save(Condominius=Condominius)

    permission_classes = [IsAuthenticated]