import datetime

from updates.managers import BaseTemporaryCreatableManager


class PatientManager(BaseTemporaryCreatableManager):
    TEMPORARY_DEFAULTS = {
        "first_name": "TMP",
        "last_name": "TMP",
        "birth_date": datetime.date(1900, 1, 1),
        "birth_number": "0000000000",
    }
