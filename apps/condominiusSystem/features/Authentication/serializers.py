from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Role


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, min_length=8)

	class Meta:
		model = User
		fields = ["id", "username", "email", "first_name", "last_name", "password"]
		read_only_fields = ["id"]

	def validate_email(self, value):
		if User.objects.filter(email__iexact=value).exists():
			raise serializers.ValidationError("Este e-mail já está cadastrado.")
		return value

	def create(self, validated_data):
		password = validated_data.pop("password")
		user = User(**validated_data, role=Role.CLIENT)
		user.set_password(password)
		user.save()
		return user


class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "username", "email", "first_name", "last_name", "role", "is_superuser"]


class UserManagementSerializer(serializers.ModelSerializer):
	role = serializers.ChoiceField(choices=Role.choices)

	class Meta:
		model = User
		fields = ["id", "username", "email", "first_name", "last_name", "role"]
		read_only_fields = ["id"]

	def validate_email(self, value):
		if User.objects.filter(email__iexact=value).exclude(pk=self.instance.pk).exists():
			raise serializers.ValidationError("Este e-mail já está cadastrado.")
		return value
