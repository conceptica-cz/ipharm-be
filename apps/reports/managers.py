from updates.managers import BaseUpdatableManager


class ReportVariableManager(BaseUpdatableManager):
    """
    Manager for ReportVariable model.
    """

    def as_dict(self):
        """
        Returns a dictionary representation of the ReportVariable model.
        """
        queryset = self.get_queryset()
        variables = {variable.name: variable.casted_value for variable in queryset}
        return variables
