from unittest.mock import patch

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.test import APITestCase
from users.models import User

from factories.users import UserFactory


class LoginBasicTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user("test_user", password="password")
        self.user.add_to_ipharm_group()

    def test_login__valid_user__token_does_not_exist(self):
        response = self.client.post(
            reverse("users:login_basic"),
            data={"username": "test_user", "password": "password"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        user_token = Token.objects.get(user=self.user)
        self.assertEqual(response.data["token"], user_token.key)

    def test_login__valid_user_token_exists(self):
        user_token = Token.objects.create(user=self.user)
        response = self.client.post(
            reverse("users:login_basic"),
            data={"username": "test_user", "password": "password"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data["token"], user_token.key)

    def test_login__invalid_username(self):
        response = self.client.post(
            reverse("users:login_basic"),
            data={"username": "does_not_exist", "password": "password"},
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg=response.data
        )
        self.assertEqual(response.data["detail"].code, "UserDoesNotExist")

    def test_login__invalid_password(self):
        response = self.client.post(
            reverse("users:login_basic"),
            data={"username": "test_user", "password": "invalid_password"},
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg=response.data
        )
        self.assertEqual(response.data["detail"].code, "IncorectPassword")

    def test_login__user_not_belonging_to_ipharm_has_no_permission(self):
        self.user.groups.clear()

        response = self.client.post(
            reverse("users:login_basic"),
            data={"username": "test_user", "password": "password"},
        )

        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data
        )
        self.assertEqual(response.data["detail"].code, "PermissionDenied")

    def test_login__super_user_permission(self):
        self.user.groups.clear()
        self.user.is_superuser = True
        self.user.save()

        response = self.client.post(
            reverse("users:login_basic"),
            data={"username": "test_user", "password": "password"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        user_token = Token.objects.get(user=self.user)
        self.assertEqual(response.data["token"], user_token.key)


class LoginKerberosTest(APITestCase):
    def setUp(self) -> None:
        pass

    @override_settings(LDAP_SKIP_AUTH=True)
    def test_login__non_existent_user_authenticated_with_kerberos_ldap_disabled(self):
        response = self.client.post(
            reverse("users:login_kerberos"),
            HTTP_X_REMOTE_USER="test_user",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        user = User.objects.get(username="test_user")
        user_token = Token.objects.get(user=user)
        self.assertEqual(response.data["token"], user_token.key)

    @override_settings(LDAP_SKIP_AUTH=True)
    def test_login__existent_user_authenticated_with_kerberos_ldap_disabled(self):
        user = UserFactory(username="test_user")
        response = self.client.post(
            reverse("users:login_kerberos"),
            HTTP_X_REMOTE_USER="test_user",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        user_token = Token.objects.get(user=user)
        self.assertEqual(response.data["token"], user_token.key)

    @patch("users.views.logins.Ldap")
    @override_settings(LDAP_SKIP_AUTH=False)
    def test_login__authorized_with_ldap(self, mocked_ldap):
        """Test that a user that is authenticated and authorized return token"""

        def mock_check_user(user):
            user.add_to_ipharm_group()

        mocked_ldap.return_value.check_user.side_effect = mock_check_user

        user = UserFactory(username="test_user")
        response = self.client.post(
            reverse("users:login_kerberos"),
            HTTP_X_REMOTE_USER="test_user",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        user_token = Token.objects.get(user=user)
        self.assertEqual(response.data["token"], user_token.key)

    @patch("users.views.logins.Ldap")
    @override_settings(LDAP_SKIP_AUTH=False)
    @override_settings(ENABLE_KERBEROS=True)
    def test_login__not_authorized_with_ldap(self, mocked_ldap):
        """Test that a user that is authenticated but not authorized return 403"""

        user = UserFactory(username="test_user")
        response = self.client.post(
            reverse("users:login_kerberos"),
            HTTP_X_REMOTE_USER="test_user",
        )
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data
        )
