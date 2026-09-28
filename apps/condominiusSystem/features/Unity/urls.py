from rest_framework.routers import DefaultRouter

from .views import UnityViewSet


router = DefaultRouter()

router.register("unidades", UnityViewSet, basename="unidade")

urlpatterns = router.urls