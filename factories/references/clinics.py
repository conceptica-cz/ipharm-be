import factory
from references.models.clinics import Clinic, Department

CLINICS = [
    {
        "id": 1,
        "abbrev": "ARO",
        "descr": "Anesteziologicko-resuscitační",
    },
    {
        "id": 3,
        "abbrev": "DER",
        "descr": "Dermatovenerologická klinika",
    },
    {
        "id": 4,
        "abbrev": "FBLR",
        "descr": "Oddělení fyziatrie, balneologie",
    },
    {
        "id": 5,
        "abbrev": "GYN",
        "descr": "Gynekologicko-porodnická klinika",
    },
    {
        "id": 6,
        "abbrev": "CHD",
        "descr": "Oddělení dětské chirurgie",
    },
    {
        "id": 7,
        "abbrev": "CHIR",
        "descr": "Chirurgická klinika",
    },
]


class ClinicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clinic
        django_get_or_create = ["reference_id"]

    external_id = factory.Iterator([c["id"] for c in CLINICS])
    reference_id = factory.Iterator([c["id"] for c in CLINICS])
    abbreviation = factory.Iterator([c["abbrev"] for c in CLINICS])
    description = factory.Iterator([c["descr"] for c in CLINICS])
    is_hospital = True
    is_ambulance = True


class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department
        django_get_or_create = ["external_id"]

    clinic = factory.SubFactory(ClinicFactory)
    external_id = factory.Iterator(range(1, 60))
    abbreviation = factory.LazyAttribute(lambda o: f"ODD{o.external_id}")
    description = factory.LazyAttribute(lambda o: f"Oddělení {o.external_id}")
    specialization_code = factory.LazyAttribute(lambda o: f"{o.external_id}")
    icp = factory.LazyAttribute(lambda o: f"{o.external_id}")
    workplace_code = factory.LazyAttribute(lambda o: f"{o.external_id}")
    for_insurance = None
