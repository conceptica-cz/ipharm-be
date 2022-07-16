from django.test import TestCase

from factories.users import UserFactory


class UserTestCase(TestCase):
    def test_add_ipharm_group(self):
        user = UserFactory()

        user.add_to_ipharm_group()

        self.assertTrue(user.groups.filter(name="ipharm").exists())
