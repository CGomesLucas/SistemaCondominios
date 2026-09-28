from rest_framework.routers import DefaultRouter

from .views import ChargeViewSet


router = DefaultRouter()
router.register("cobrancas", ChargeViewSet, basename="cobranca")

urlpatterns = router.urls