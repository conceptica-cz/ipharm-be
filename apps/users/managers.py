from django.contrib.auth.models import UserManager as BaseUserManager
from django.db.models import Manager


class UserManager(BaseUserManager):
    def get_updater_user(self):
        """Get or create the updater user"""
        user, _ = self.get_or_create(username="updater", defaults={"is_system": True})
        return user
