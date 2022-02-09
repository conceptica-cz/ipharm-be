import datetime

from updates.managers import BaseTemporaryCreatableManager


class PatientManager(BaseTemporaryCreatableManager):
    TEMPORARY_DEFAULTS = {
        "first_name": "TMP",
        "last_name": "TMP",
        "birth_date": datetime.date(1900, 1, 1),
        "birth_number": "0000000000",
    }

    def update_names(self):
        for patient in self.get_queryset().filter(
            first_name__isnull=True, last_name__isnull=True
        ):
            patient.first_name = patient.name.split(" ", 1)[1]
            patient.last_name = patient.name.split(" ", 1)[0]
            patient.save()
