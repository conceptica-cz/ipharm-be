from updates.managers import BaseTemporaryCreatableManager


class DiagnosisManager(BaseTemporaryCreatableManager):
    TEMPORARY_DEFAULTS = {
        "name": "TMP",
    }

    def only_via_api(self):
        return self.filter(carediagnosis__via_api=True)
