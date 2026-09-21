from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Condominius
from .serializers import CondominiusSerializer


class CondominiusViewSet(ModelViewSet):
    queryset = Condominius.objects.all()
    serializer_class = CondominiusSerializer

    permission_classes = [IsAuthenticated]