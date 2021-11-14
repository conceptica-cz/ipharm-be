from updates.managers import BaseTemporaryCreatableManager, BaseUpdatableManager


class PersonManager(BaseTemporaryCreatableManager):
    TEMPORARY_DEFAULTS = {
        "name": "TMP",
        "f_title": "TMP",
        "l_title": "TMP",
    }
