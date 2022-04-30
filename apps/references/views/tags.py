from references.models import Tag
from references.serializers import TagSerializer
from rest_framework import filters, generics


class TagListView(generics.ListAPIView):
    """Tag list"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class TagDetailView(generics.RetrieveAPIView):
    """Tag detail"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
