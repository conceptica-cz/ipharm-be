import datetime
import random

import factory
from factory import fuzzy
from ipharm.models import Care, Dekurz

from factories.ipharm.patients import PatientFactory
from factories.references.clinics import ClinicFactory, DepartmentFactory
from factories.references.diagnoses import DiagnosisFactory
from factories.references.persons import PersonFactory


class CareFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Care
        django_get_or_create = ("external_id",)

    class Params:
        finished_at_decider = factory.LazyFunction(lambda: bool(random.randint(0, 8)))

    patient = factory.SubFactory(PatientFactory)
    care_type = factory.Iterator([Care.HOSPITALIZATION, Care.AMBULATION])
    is_active = True
    main_diagnosis = factory.SubFactory(DiagnosisFactory)
    external_id = factory.Sequence(lambda n: n)

    clinic = factory.SubFactory(ClinicFactory)
    department = factory.SubFactory(
        DepartmentFactory, clinic=factory.SelfAttribute("..clinic")
    )
    started_at = fuzzy.FuzzyDateTime(
        datetime.datetime(2021, 9, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2021, 10, 1, tzinfo=datetime.timezone.utc),
    )
    finished_at = factory.Maybe(
        "datetime_out_decider",
        yes_declaration=None,
        no_declaration=factory.fuzzy.FuzzyDateTime(
            datetime.datetime(2021, 10, 1, tzinfo=datetime.timezone.utc),
            datetime.datetime(2021, 11, 1, tzinfo=datetime.timezone.utc),
        ),
    )

    @factory.post_generation
    def patient_care(self, create, extracted, **kwargs):
        if create:
            self.patient.set_current_care(self)

    @factory.post_generation
    def last_dekurz(self, create, extracted, **kwargs):
        if create:
            for _ in range(random.randint(1, 5)):
                self.set_last_dekurz(
                    DekurzFactory(care=self, department=self.department)
                )


class DekurzFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dekurz

    care = factory.SubFactory(CareFactory)
    made_at = fuzzy.FuzzyDateTime(
        datetime.datetime(2021, 9, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2021, 11, 1, tzinfo=datetime.timezone.utc),
    )
    doctor = factory.SubFactory(PersonFactory)
    department = factory.SubFactory(DepartmentFactory)
