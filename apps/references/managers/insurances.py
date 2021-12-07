from updates.managers import BaseTemporaryCreatableManager


class InsuranceCompanyManager(BaseTemporaryCreatableManager):
    TEMPORARY_DEFAULTS = {
        "name": "TMP",
        "f_title": "TMP",
        "l_title": "TMP",
    }

    def get_temporary_defaults(self, **kwargs) -> dict:
        code = kwargs["code"]
        return {
            "name": f"TMP {code}",
            "shortcut": f"TMP {code}",
            "address": "TMP",
            "zip": "TMP",
            "city": "TMP",
        }
