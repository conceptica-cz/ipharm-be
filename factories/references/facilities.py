import factory
from references.models import MedicalFacility


class MedicalFacilityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MedicalFacility
        django_get_or_create = ["facility_id"]

    facility_id = factory.Sequence(lambda n: n)
    code = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: n)
