from rest_framework.generics import RetrieveUpdateAPIView

from users.models import User
from users.serializers import UserSerializer


class UserView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
