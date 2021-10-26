import datetime
import random

import factory
from factory import fuzzy
from faker import Faker
from ipharm.models import patients

from factories.references.clinics import ClinicFactory


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
    datetime_in = fuzzy.FuzzyDateTime(
        datetime.datetime(2021, 9, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2021, 10, 1, tzinfo=datetime.timezone.utc),
    )
    datetime_out = factory.Maybe(
        "datetime_out_decider",
        yes_declaration=None,
        no_declaration=factory.fuzzy.FuzzyDateTime(
            datetime.datetime(2021, 10, 1, tzinfo=datetime.timezone.utc)
        ),
    )
    diagnosis = factory.LazyFunction(
        lambda: f"{Faker().pystr(1, 1)}{Faker().pyint(100, 999)}"
    )
    dekurz_datetime = fuzzy.FuzzyDateTime(
        datetime.datetime(2021, 9, 1, tzinfo=datetime.timezone.utc)
    )
    dekurz_who = fuzzy.FuzzyInteger(10000, 99999)
    dekurz_department = fuzzy.FuzzyInteger(10000, 99999)
