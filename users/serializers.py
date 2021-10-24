from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "clinics"]
        extra_kwargs = {"username": {"read_only": True}}
