from django.conf import settings
from updates.managers import BaseUpdatableManager


class IdentificationManager(BaseUpdatableManager):
    """
    Manager for the IdentificationMna model.
    """

    def get_identification_for_insurance_report(self):
        """Returns the identification using the insurance report."""
        return self.get(for_insurance=True)
