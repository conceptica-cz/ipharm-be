from references.models import Tag
from references.serializers import TagSerializer
from rest_framework import filters, generics


class TagListView(generics.ListCreateAPIView):
    """Tag list"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Tag detail"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
