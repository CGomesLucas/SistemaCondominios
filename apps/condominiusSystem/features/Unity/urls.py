from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import UnityCreateView, UnityViewSet


router = DefaultRouter()

router.register("unidades", UnityViewSet, basename="unidade")

urlpatterns = [
	path(
		"condominios/<int:condominio_id>/unidades/",
		UnityCreateView.as_view(),
		name="unidade-create",
	),
	*router.urls,
]