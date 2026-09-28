from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserProfileSerializer, UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
	serializer_class = UserRegistrationSerializer
	permission_classes = [AllowAny]
	authentication_classes = []


class CurrentUserView(APIView):
	def get(self, request):
		return Response(UserProfileSerializer(request.user).data)
