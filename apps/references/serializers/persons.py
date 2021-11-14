from rest_framework import serializers

from ..models.persons import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = read_only_fields = (
            "id",
            "person_number",
            "name",
            "f_title",
            "l_title",
        )
