import datetime
import random

import factory
from factory import fuzzy
from faker import Faker
from ipharm.models import Patient, patients

from factories.references.clinics import ClinicFactory, DepartmentFactory
from factories.references.diagnoses import DiagnosisFactory
from factories.references.insurances import InsuranceCompanyFactory
from factories.references.persons import PersonFactory


class PatientWithoutDiagnosisFactory(factory.django.DjangoModelFactory):
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
    patient_type = factory.Iterator([Patient.HOSPITAL, Patient.AMBULANCE])

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

    insurance_company = factory.SubFactory(InsuranceCompanyFactory)
    insurance_number = fuzzy.FuzzyInteger(1000000000, 9999999999)
    height = fuzzy.FuzzyInteger(130, 210)
    weight = factory.LazyAttribute(lambda obj: obj.height - 100 + Faker().pyint(0, 40))
    department_in = factory.SubFactory(DepartmentFactory)
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
    dekurz_datetime = fuzzy.FuzzyDateTime(
        datetime.datetime(2021, 9, 1, tzinfo=datetime.timezone.utc)
    )
    dekurz_who = factory.SubFactory(PersonFactory)
    dekurz_department = factory.SubFactory(DepartmentFactory)


class PatientDiagnosisFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = patients.PatientDiagnosis
        django_get_or_create = ["patient", "diagnosis"]

    patient = factory.SubFactory(PatientWithoutDiagnosisFactory)
    diagnosis = factory.SubFactory(DiagnosisFactory)
    via_api = True


class PatientFactory(PatientWithoutDiagnosisFactory):
    patient_diagnosis = factory.RelatedFactory(
        PatientDiagnosisFactory,
        factory_related_name="patient",
    )
