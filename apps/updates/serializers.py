from rest_framework import serializers
from users.serializers import UserLightSerializer


class FieldChangeSerializer(serializers.Serializer):
    field = serializers.CharField(max_length=255)
    old_value = serializers.CharField(max_length=255, source="old")
    new_value = serializers.CharField(max_length=255, source="new")
    many_to_many_entity = serializers.CharField(max_length=255, required=False)


class ModelChangeSerializer(serializers.Serializer):
    user = UserLightSerializer()
    date = serializers.DateTimeField()
    entity_name = serializers.CharField(max_length=255)
    entity_id = serializers.IntegerField()
    field_changes = FieldChangeSerializer(many=True)
