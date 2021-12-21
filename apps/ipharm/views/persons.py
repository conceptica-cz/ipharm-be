from references.models.persons import Person
from references.serializers.persons import PersonSerializer
from rest_framework import filters, generics


class PersonListView(generics.ListAPIView):
    """Person list"""

    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonDetailView(generics.RetrieveAPIView):
    """Person detail"""

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
