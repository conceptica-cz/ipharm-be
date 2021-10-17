import datetime
import random

import factory
from factory import fuzzy
from faker import Faker

from ipharm.models import patients

CLINICS = [
    {"id": 1, "abbrev": "ARO", "descr": "Anesteziologicko-resuscitační"},
    {"id": 3, "abbrev": "DER", "descr": "Dermatovenerologická klinika"},
    {"id": 4, "abbrev": "FBLR", "descr": "Oddělení fyziatrie, balneologie"},
    {"id": 5, "abbrev": "GYN", "descr": "Gynekologicko-porodnická klinika"},
    {"id": 6, "abbrev": "CHD", "descr": "Oddělení dětské chirurgie"},
    {"id": 7, "abbrev": "CHIR", "descr": "Chirurgická klinika"},
    {"id": 8, "abbrev": "CHP", "descr": "Oddělení plastické chirurgie"},
    {"id": 10, "abbrev": "INT", "descr": "Interní oddělení"},
    {"id": 11, "abbrev": "INF", "descr": "Infekční klinika"},
    {"id": 14, "abbrev": "NEU", "descr": "Neurologické oddělení"},
    {"id": 16, "abbrev": "OFT", "descr": "Oční oddělení"},
    {"id": 24, "abbrev": "ORL", "descr": "Ušní-nosní-krční oddělení"},
    {"id": 25, "abbrev": "ORT", "descr": "Ortopedická klinika"},
    {"id": 28, "abbrev": "PED", "descr": "Dětské oddělení"},
    {"id": 29, "abbrev": "PNEU", "descr": "Klinika pneumologie"},
    {"id": 32, "abbrev": "RAD", "descr": "Ústav radiační onkologie"},
    {"id": 33, "abbrev": "RTG", "descr": "Radiodiagnostická klinika"},
    {"id": 34, "abbrev": "NEO", "descr": "Neonatologie"},
    {"id": 37, "abbrev": "URO", "descr": "Urologické oddělení"},
    {"id": 41, "abbrev": "N1OLH", "descr": "Oddělení následné péče"},
    {"id": 43, "abbrev": "DIOP", "descr": "Lůžka DIOP"},
]


class ClinicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = patients.Clinic
        django_get_or_create = ["clinic_id", "abbreviation", "description"]

    clinic_id = factory.Iterator([c["id"] for c in CLINICS])
    abbreviation = factory.Iterator([c["abbrev"] for c in CLINICS])
    description = factory.Iterator([c["descr"] for c in CLINICS])


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = patients.Patient
        django_get_or_create = ["record_id", "patient_id"]

    class Params:
        first_name_male = factory.Faker("first_name_male", locale="cs")
        last_name_male = factory.Faker("last_name_male", locale="cs")
        first_name_female = factory.Faker("first_name_female", locale="cs")
        last_name_female = factory.Faker("last_name_female", locale="cs")
        datetime_out_decider = factory.LazyFunction(lambda: bool(random.randint(0, 8)))
        gender = factory.Iterator(["MALE", "FEMALE"])

    clinic = factory.SubFactory(ClinicFactory)
    record_id = factory.Sequence(lambda n: n)
    patient_id = factory.Sequence(lambda n: n)

    @factory.lazy_attribute
    def first_name(self):
        if self.gender == "MALE":
            return self.first_name_male
        else:
            return self.first_name_female

    @factory.lazy_attribute
    def last_name(self):
        if self.gender == "MALE":
            return self.last_name_male
        else:
            return self.last_name_female

    birth_date = factory.Faker("date_of_birth", minimum_age=18, maximum_age=95)

    @factory.lazy_attribute
    def birth_number(self):
        birth = self.birth_date.strftime("%y%m%d")
        return f"{birth}{Faker().pyint(1000, 9999)}"

    insurance_company = "111"
    insurance_number = fuzzy.FuzzyInteger(1000000000, 9999999999)
    height = fuzzy.FuzzyInteger(130, 210)
    weight = factory.LazyAttribute(lambda obj: obj.height - 100 + Faker().pyint(0, 40))
    department_in_id = fuzzy.FuzzyInteger(1, 15)
    datetime_in = fuzzy.FuzzyDate(datetime.date(2021, 9, 1), datetime.date(2021, 10, 1))
    datetime_out = factory.Maybe(
        "datetime_out_decider",
        yes_declaration=None,
        no_declaration=factory.fuzzy.FuzzyDate(datetime.date(2021, 10, 1)),
    )
    diagnosis = factory.LazyFunction(
        lambda: f"{Faker().pystr(1, 1)}{Faker().pyint(100, 999)}"
    )
    dekurz_datetime = fuzzy.FuzzyDate(datetime.date(2021, 9, 1))
    dekurz_who = fuzzy.FuzzyInteger(10000, 99999)
    dekurz_department = fuzzy.FuzzyInteger(10000, 99999)
