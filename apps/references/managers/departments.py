from updates.managers import BaseTemporaryCreatableManager


class DepartmentForReportNotFound(Exception):
    pass


class DepartmentManager(BaseTemporaryCreatableManager):
    TEMPORARY_DEFAULTS = {
        "abbreviation": "TMP",
        "description": "TMP",
        "specialization_code": "TMP",
        "icp": "TMP",
    }

    def get_department_for_insurance_report(self):
        """Returns the department using the insurance report."""
        try:
            department = self.get(for_insurance=True)
        except self.model.DoesNotExist:
            raise DepartmentForReportNotFound()
        return department
