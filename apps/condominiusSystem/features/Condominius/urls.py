from rest_framework.routers import DefaultRouter

from .views import CondominiusViewSet


router = DefaultRouter()

router.register("condominius", CondominiusViewSet)

urlpatterns = router.urls