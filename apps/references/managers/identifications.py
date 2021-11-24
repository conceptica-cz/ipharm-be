from django.conf import settings
from updates.managers import BaseUpdatableManager


class IdentificationManager(BaseUpdatableManager):
    """
    Manager for the IdentificationMna model.
    """

    def get_our_identification(self):
        """
        Returns the identification of the current user.
        """
        return self.get_queryset().get(identifier=settings.OUR_HEALTH_CARE_IDENTIFIER)
