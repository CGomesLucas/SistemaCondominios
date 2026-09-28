from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdmin
from .serializers import (
	UserManagementSerializer,
	UserProfileSerializer,
	UserRegistrationSerializer,
)


class UserRegistrationView(generics.CreateAPIView):
	serializer_class = UserRegistrationSerializer
	permission_classes = [IsAdmin]


class UserManagementView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = UserManagementSerializer
	permission_classes = [IsAdmin]
	queryset = UserManagementSerializer.Meta.model.objects.all()


class CurrentUserView(APIView):
	def get(self, request):
		return Response(UserProfileSerializer(request.user).data)
