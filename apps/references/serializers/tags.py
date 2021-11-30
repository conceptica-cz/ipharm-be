from rest_framework import serializers

from ..models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ["is_deleted"]
        read_only_fields = ["id"]
