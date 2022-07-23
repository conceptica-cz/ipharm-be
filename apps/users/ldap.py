import logging

from django.conf import settings
from django.contrib.auth.models import Group
from ldap3 import ALL_ATTRIBUTES, Connection, Server

logger = logging.getLogger(__name__)


class Ldap:
    def __init__(self):
        self.server = None
        self.conn = None

    def connect(self):
        self.server = Server(settings.LDAP_URL)
        self.conn = Connection(
            server=self.server,
            user=settings.LDAP_CONNECTION_USERNAME,
            password=settings.LDAP_CONNECTION_PASSWORD,
            auto_bind=True,
        )

    def check_user(self, user):
        search_base = settings.LDAP_SEARCH_BASE
        for group_name, search_filter in settings.LDAP_GROUPS_MAP.items():
            self._update_user(user, group_name, search_base, search_filter)

    def _update_user(
        self, user, group_name, search_base: str, search_filter: str
    ) -> bool:
        """
        Search for a user in LDAP. Update the local user if found.

        :param user: The user to search and update.
        :param group_name: The name of the group to add to the user.
        :param search_base:  The search base.
        :param search_filter: The filter to use to search user in LDAP.
        :return: True if the user exists, False otherwise.
        """
        username = user.username.split("@")[0]
        search_filter = search_filter.format(username)
        self.conn.search(
            search_base=search_base,
            search_filter=search_filter,
            attributes=ALL_ATTRIBUTES,
        )
        if len(self.conn.entries) != 1:
            logger.info(
                "User not found in LDAP",
                extra={"user_id": user.id, "username": user.username},
            )
            return False

        entry = self.conn.entries[0]

        for field, ldap_field in settings.LDAP_USER_FIELDS.items():
            setattr(user, field, getattr(entry, ldap_field))
        user.save()

        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        logger.debug(
            "User was found in LDAP and updated",
            extra={"user_id": user.id, "username": user.username},
        )

        return True
