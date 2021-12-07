from updates.managers import BaseTemporaryCreatableManager


class DepartmentManager(BaseTemporaryCreatableManager):
    TEMPORARY_DEFAULTS = {
        "abbreviation": "TMP",
        "description": "TMP",
        "specialty": "TMP",
        "icp": "TMP",
    }
