from rest_framework import viewsets

from apps.condominiusSystem.features.Authentication.permissions import IsAdminOrReadOnly

from .filters import ChargeFilter
from .models import Charge
from .serializers import ChargeSerializer


class ChargeViewSet(viewsets.ModelViewSet):
    queryset = Charge.objects.select_related("unidade", "unidade__condominio").all()
    serializer_class = ChargeSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = ChargeFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        Charge.objects.refresh_overdue()
        return queryset