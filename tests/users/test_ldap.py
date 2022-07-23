from unittest.mock import Mock, patch

from django.test import TestCase, override_settings
from ldap3 import ALL_ATTRIBUTES, Connection
from users.ldap import Ldap

from factories.users import UserFactory


@override_settings(LDAP_GROUPS_MAP={"ipharm": "(&(uid={})(memberOf=cn=employees*))"})
@override_settings(LDAP_USER_FIELDS={"email": "mail"})
@override_settings(LDAP_SEARCH_BASE="dc=example,dc=com")
class LdapTestCase(TestCase):
    def test_check_user__exists(self):
        ldap = Ldap()
        ldap.conn = Mock(spec=Connection)
        ldap.conn.search.return_value = True
        ldap.conn.entries = [
            Mock(mail="user_42@example.com", uid="user", cn="User", sn="User")
        ]
        user = UserFactory(username="test_user@EXAMPLE.COM")

        ldap.check_user(user)

        self.assertTrue(user.groups.filter(name="ipharm").exists())
        self.assertEqual(user.email, "user_42@example.com")
        ldap.conn.search.assert_called_once_with(
            search_base="dc=example,dc=com",
            search_filter="(&(uid=test_user)(memberOf=cn=employees*))",
            attributes=ALL_ATTRIBUTES,
        )

    def test_check_user__not_exists(self):
        ldap = Ldap()
        ldap.conn = Mock(spec=Connection)
        ldap.conn.search.return_value = False
        ldap.conn.entries = []
        user = UserFactory(username="test_user@EXAMPLE.COM")

        ldap.check_user(user)

        self.assertFalse(user.groups.filter(name="ipharm").exists())
        self.assertNotEqual(user.email, "user_42@example.com")
        ldap.conn.search.assert_called_once_with(
            search_base="dc=example,dc=com",
            search_filter="(&(uid=test_user)(memberOf=cn=employees*))",
            attributes=ALL_ATTRIBUTES,
        )
