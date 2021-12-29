from rest_framework import views
from rest_framework.response import Response
from updates.serializers import ModelChangeSerializer


class HistoryView(views.APIView):
    queryset = None

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        obj = self.queryset.get(pk=pk)
        changes = obj.get_changes()
        serializer = ModelChangeSerializer(changes, many=True)
        return Response(serializer.data)
