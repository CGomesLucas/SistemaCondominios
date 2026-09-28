from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import CurrentUserView, UserManagementView, UserRegistrationView

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('registro/', UserRegistrationView.as_view(), name='user_registration'),
    path('usuarios/<int:pk>/', UserManagementView.as_view(), name='user_management'),
    path('me/', CurrentUserView.as_view(), name='current_user'),
]