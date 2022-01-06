import factory
from references.models import MedicalProcedure


class MedicalProcedureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MedicalProcedure

    code = factory.Iterator(["05751", "05752", "05753", "05755"])
    name = ""
    scores = 0.0
