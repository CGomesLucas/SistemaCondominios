from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from apps.condominiusSystem.features.Authentication.permissions import IsAdminOrReadOnly

from .filters import AgreementFilter
from .models import Agreement, AgreementInstallment
from .serializers import AgreementInstallmentSerializer, AgreementSerializer


class AgreementViewSet(viewsets.ModelViewSet):
    queryset = Agreement.objects.select_related("unidade").prefetch_related(
        "cobrancas",
        "parcelas",
    )
    serializer_class = AgreementSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = AgreementFilter


class AgreementInstallmentViewSet(viewsets.ModelViewSet):
    queryset = AgreementInstallment.objects.select_related("acordo", "acordo__unidade")
    serializer_class = AgreementInstallmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["acordo", "status"]

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed(
            "POST",
            detail="As parcelas são geradas automaticamente ao criar ou alterar o cronograma do acordo.",
        )

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(
            "DELETE",
            detail="As parcelas geradas fazem parte do cronograma do acordo e não podem ser excluídas individualmente.",
        )