from updates.managers import BaseUpdatableManager


class ReportVariableManager(BaseUpdatableManager):
    """
    Manager for ReportVariable model.
    """

    def as_dict(self, report_type=None):
        """
        Returns a dictionary representation of the ReportVariable model.
        """
        queryset = self.get_queryset()
        if report_type:
            queryset = queryset.filter(report_type=report_type)
        variables = {variable.name: variable.casted_value for variable in queryset}
        return variables
