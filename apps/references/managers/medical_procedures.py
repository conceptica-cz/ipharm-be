from updates.managers import BaseUpdatableManager


class MedicalProcedureManager(BaseUpdatableManager):
    """
    Manager for the MedicalProcedure model.
    """

    def get_procedure_by_code(self, code: str) -> "MedicalProcedure":
        return self.get(code=code)
