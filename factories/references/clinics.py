import factory
from references.models.clinics import Clinic

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
    {
        "id": 8,
        "abbrev": "CHP",
        "descr": "Oddělení plastické chirurgie",
    },
    {
        "id": 10,
        "abbrev": "INT",
        "descr": "Interní oddělení",
    },
    {
        "id": 11,
        "abbrev": "INF",
        "descr": "Infekční klinika",
    },
    {
        "id": 14,
        "abbrev": "NEU",
        "descr": "Neurologické oddělení",
    },
    {
        "id": 16,
        "abbrev": "OFT",
        "descr": "Oční oddělení",
    },
    {
        "id": 24,
        "abbrev": "ORL",
        "descr": "Ušní-nosní-krční oddělení",
    },
    {
        "id": 25,
        "abbrev": "ORT",
        "descr": "Ortopedická klinika",
    },
    {
        "id": 28,
        "abbrev": "PED",
        "descr": "Dětské oddělení",
    },
    {
        "id": 29,
        "abbrev": "PNEU",
        "descr": "Klinika pneumologie",
    },
    {
        "id": 32,
        "abbrev": "RAD",
        "descr": "Ústav radiační onkologie",
    },
    {
        "id": 33,
        "abbrev": "RTG",
        "descr": "Radiodiagnostická klinika",
    },
    {
        "id": 34,
        "abbrev": "NEO",
        "descr": "Neonatologie",
    },
    {
        "id": 37,
        "abbrev": "URO",
        "descr": "Urologické oddělení",
    },
    {
        "id": 41,
        "abbrev": "N1OLH",
        "descr": "Oddělení následné péče",
    },
    {
        "id": 43,
        "abbrev": "DIOP",
        "descr": "Lůžka DIOP",
    },
]

AMBULANCES = [
    {
        "id": 1,
        "abbrev": "AMB1",
        "descr": "Ambulance N1",
    },
    {
        "id": 2,
        "abbrev": "AMB2",
        "descr": "Ambulance N2",
    },
    {
        "id": 3,
        "abbrev": "AMB3",
        "descr": "Ambulance N3",
    },
    {
        "id": 4,
        "abbrev": "AMB4",
        "descr": "Ambulance N4",
    },
    {
        "id": 5,
        "abbrev": "AMB5",
        "descr": "Ambulance N5",
    },
]


class ClinicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clinic
        django_get_or_create = ["clinic_id", "clinic_type"]

    clinic_id = factory.Iterator([c["id"] for c in CLINICS])
    abbreviation = factory.Iterator([c["abbrev"] for c in CLINICS])
    description = factory.Iterator([c["descr"] for c in CLINICS])
    clinic_type = Clinic.CLINIC


class AmbulanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clinic
        django_get_or_create = ["clinic_id", "clinic_type"]

    clinic_id = factory.Iterator([c["id"] for c in AMBULANCES])
    abbreviation = factory.Iterator([c["abbrev"] for c in AMBULANCES])
    description = factory.Iterator([c["descr"] for c in AMBULANCES])
    clinic_type = Clinic.AMBULANCE
