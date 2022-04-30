from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import SAFE_METHODS
from users.models import User
from users.serializers import UserSerializer, UserWriteSerializer


class UserView(RetrieveUpdateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return UserSerializer
        else:
            return UserWriteSerializer

    def get_object(self):
        return self.request.user
