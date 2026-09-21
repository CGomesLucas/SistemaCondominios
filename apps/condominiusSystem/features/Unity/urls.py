from rest_framework.routers import DefaultRouter

from .views import UnityViewset


router = DefaultRouter()

router.register("unitys", UnityViewset)

urlpatterns = router.urls