from rest_framework import serializers

from ..models import Drug


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = read_only_fields = (
            "id",
            "code_sukl",
            "name",
        )
