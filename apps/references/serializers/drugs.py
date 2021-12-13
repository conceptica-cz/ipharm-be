from rest_framework import serializers

from ..models import Drug


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        exclude = ("is_deleted",)
        read_only_fields = ("id",)
