from updates.managers import BaseUpdatableManager


class IdentificationForReportNotFound(Exception):
    pass


class IdentificationManager(BaseUpdatableManager):
    """
    Manager for the IdentificationMna model.
    """

    def get_identification_for_insurance_report(self):
        """Returns the identification using the insurance report."""
        try:
            identification = self.get(for_insurance=True)
        except self.model.DoesNotExist:
            raise IdentificationForReportNotFound()
        return identification
