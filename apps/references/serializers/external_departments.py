from rest_framework import serializers

from ..models import ExternalDepartment


class ExternalDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalDepartment
        exclude = ("is_deleted",)
        read_only_fields = ("id",)
