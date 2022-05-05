from django.db.models import Manager, QuerySet
from django.utils import timezone
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


class GenericReportFileQuerySet(QuerySet):
    """
    QuerySet for the GenericReportFile model.
    """

    def old_files(self):
        """
        Returns a queryset of files that are older than the one day.
        """
        min_date = timezone.now() - timezone.timedelta(days=1)
        return self.filter(created_at__lt=min_date)


class GenericReportFileManager(Manager):
    """
    Manager for the GenericReportFile model.
    """

    def delete_old_files(self):
        for file in self.old_files():
            file.delete()
