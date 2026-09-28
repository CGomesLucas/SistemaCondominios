from rest_framework.viewsets import ModelViewSet

from .models import Condominius
from .serializers import CondominiusSerializer
from apps.condominiusSystem.features.Authentication.permissions import IsAdminOrReadOnly


class CondominiusViewSet(ModelViewSet):
    queryset = Condominius.objects.all()
    serializer_class = CondominiusSerializer

    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["name", "type_condominious", "cidade", "uf"]