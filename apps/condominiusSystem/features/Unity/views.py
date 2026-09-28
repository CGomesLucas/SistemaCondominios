from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers, viewsets
from rest_framework.exceptions import MethodNotAllowed

from apps.condominiusSystem.features.Authentication.permissions import IsAdminOrReadOnly
from apps.condominiusSystem.features.Condominius.models import Condominius

from .models import Unity
from .serializers import UnityNestedCreateSerializer, UnitySerializer


class UnityCreateView(generics.CreateAPIView):
    queryset = Unity.objects.all()
    serializer_class = UnityNestedCreateSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_condominio(self):
        if not hasattr(self, "_condominio"):
            self._condominio = get_object_or_404(
                Condominius,
                pk=self.kwargs["condominio_id"],
            )
        return self._condominio

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["condominio"] = self.get_condominio()
        return context

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError as error:
            raise serializers.ValidationError(
                {"non_field_errors": ["Já existe uma unidade com esse bloco e número no condomínio."]}
            ) from error


class UnityViewSet(viewsets.ModelViewSet):
    queryset = Unity.objects.select_related("condominio").all()
    serializer_class = UnitySerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["condominio", "status", "building", "is_active"]

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed(
            "POST",
            detail="Informe o condomínio na URL: /api/condominios/{condominio_id}/unidades/.",
        )