from rest_framework import viewsets

from apps.condominiusSystem.features.Authentication.permissions import IsAdminOrReadOnly

from .models import Unity
from .serializers import UnitySerializer


class UnityViewSet(viewsets.ModelViewSet):
    queryset = Unity.objects.select_related("condominio").all()
    serializer_class = UnitySerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["condominio", "status", "building", "is_active"]