from references.serializers.clinics import ClinicSerializer
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    clinics = ClinicSerializer(many=True)

    class Meta:
        model = User
        fields = ["username", "clinics"]
        extra_kwargs = {"username": {"read_only": True}}


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "clinics"]
        extra_kwargs = {"username": {"read_only": True}}
