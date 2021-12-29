from references.serializers.clinics import ClinicSerializer
from rest_framework import serializers

from .models import User


class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = read_only_fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class UserSerializer(serializers.ModelSerializer):
    hospitals = ClinicSerializer(many=True)
    ambulances = ClinicSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "hospitals",
            "ambulances",
        ]
        extra_kwargs = {"username": {"read_only": True}}


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "hospitals",
            "ambulances",
        ]
        extra_kwargs = {
            "username": {"read_only": True},
            "hospitals": {"required": False, "allow_empty": True},
            "ambulances": {"required": False, "allow_empty": True},
        }
