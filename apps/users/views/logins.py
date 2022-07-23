import logging

from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import authentication, permissions, serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from users.authentication import KerberosRemoteUserAuthentication
from users.ldap import Ldap
from users.models import User
from users.serializers import BasicLoginSerializer

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        request=BasicLoginSerializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                name="token",
                fields={"token": serializers.CharField()},
            ),
        },
    ),
)
class LoginBasic(APIView):
    """
    Authenticate and check permissions for a user.
    Returns token, that can be used to authenticate further requests.

    Returns 401 if user is not authenticated.

    Returns 403 if user doesn't have permission to access the application
    (user must belong to appropriate group).

    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = BasicLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(username=serializer.validated_data["username"])
        except User.DoesNotExist:
            raise AuthenticationFailed("User does not exist", code="UserDoesNotExist")
        if not user.check_password(serializer.validated_data["password"]):
            raise AuthenticationFailed("IncorectPassword", code="IncorectPassword")
        if not self.has_permission(user):
            raise PermissionDenied("Permission denied", code="PermissionDenied")
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)

    @staticmethod
    def has_permission(user):
        if user.is_superuser or user.in_ipharm_group():
            return True
        else:
            return False


@extend_schema_view(
    post=extend_schema(
        responses={
            status.HTTP_200_OK: inline_serializer(
                name="token",
                fields={"token": serializers.CharField()},
            ),
        },
    ),
)
class LoginKerberos(APIView):
    """
    Authenticate and check permissions for a user.
    Returns token, that can be used to authenticate further requests.

    Returns 401 if user is not authenticated.

    Returns 403 if user doesn't have permission to access the application
    (user must belong to appropriate group).

    """

    authentication_classes = (KerberosRemoteUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        if settings.LDAP_SKIP_AUTH:
            logger.warning(
                "LDAP_SKIP_AUTH is set to True, skipping LDAP authentication"
            )
        else:
            ldap = Ldap()
            ldap.connect()
            ldap.check_user(user)
            if not self.has_permission(user):
                raise PermissionDenied("Permission denied", code="PermissionDenied")
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)

    @staticmethod
    def has_permission(user):
        if user.is_superuser or user.in_ipharm_group():
            return True
        else:
            return False
