from rest_framework.routers import DefaultRouter

from .views import CondominiusViewSet


router = DefaultRouter()

router.register("condominios", CondominiusViewSet, basename="condominio")

urlpatterns = router.urls