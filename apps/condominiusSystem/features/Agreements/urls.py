from rest_framework.routers import DefaultRouter

from .views import AgreementInstallmentViewSet, AgreementViewSet


router = DefaultRouter()
router.register("acordos", AgreementViewSet, basename="acordo")
router.register("parcelas-acordo", AgreementInstallmentViewSet, basename="parcela-acordo")

urlpatterns = router.urls
