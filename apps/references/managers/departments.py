from updates.managers import BaseTemporaryCreatableManager


class DepartmentManager(BaseTemporaryCreatableManager):
    TEMPORARY_DEFAULTS = {
        "abbreviation": "TMP",
        "description": "TMP",
        "specialization_code": "TMP",
        "icp": "TMP",
    }
