from rest_framework import serializers
from users.serializers import UserLightSerializer


class FieldChangeSerializer(serializers.Serializer):
    field = serializers.CharField(max_length=255)
    old_value = serializers.CharField(max_length=255, source="old")
    new_value = serializers.CharField(max_length=255, source="new")


class ModelChangeSerializer(serializers.Serializer):
    user = UserLightSerializer()
    date = serializers.DateTimeField()
    field_changes = FieldChangeSerializer(many=True)
