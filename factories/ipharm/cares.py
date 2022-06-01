import datetime
import random

import factory
from factory import fuzzy
from ipharm.models.cares import Care, Dekurz

from factories.ipharm.patients import PatientFactory
from factories.references.clinics import ClinicFactory, DepartmentFactory
from factories.references.diagnoses import DiagnosisFactory
from factories.references.external_departments import ExternalDepartmentFactory
from factories.references.persons import PersonFactory


class CareFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Care

    class Params:
        finished_at_decider = factory.LazyFunction(lambda: bool(random.randint(0, 8)))
        external_decider = factory.LazyAttribute(lambda o: o.care_type == Care.EXTERNAL)

    patient = factory.SubFactory(PatientFactory)
    care_type = factory.Iterator([Care.HOSPITALIZATION, Care.AMBULATION, Care.EXTERNAL])
    main_diagnosis = factory.SubFactory(DiagnosisFactory)

    external_id = factory.Maybe(
        "external_decider",
        yes_declaration=None,
        no_declaration=factory.Sequence(lambda n: n),
    )

    clinic = factory.SubFactory(ClinicFactory)

    department = factory.Maybe(
        "external_decider",
        yes_declaration=None,
        no_declaration=factory.SubFactory(
            DepartmentFactory, clinic=factory.SelfAttribute("..clinic")
        ),
    )

    external_department = factory.Maybe(
        "external_decider",
        yes_declaration=factory.SubFactory(ExternalDepartmentFactory),
        no_declaration=None,
    )

    doctor = factory.Maybe(
        "external_decider",
        yes_declaration=factory.Faker("name", locale="cs"),
        no_declaration=None,
    )

    started_at = fuzzy.FuzzyDateTime(
        datetime.datetime(2021, 9, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2021, 10, 1, tzinfo=datetime.timezone.utc),
    )
    finished_at = factory.Maybe(
        "finished_at_decider",
        yes_declaration=None,
        no_declaration=factory.fuzzy.FuzzyDateTime(
            datetime.datetime(2021, 10, 1, tzinfo=datetime.timezone.utc),
            datetime.datetime(2021, 11, 1, tzinfo=datetime.timezone.utc),
        ),
    )
    is_active = factory.LazyAttribute(lambda o: o.finished_at is None)

    @factory.post_generation
    def patient_care(self, create, extracted, **kwargs):
        if create:
            self.patient.set_current_care(self)

    @factory.post_generation
    def last_dekurz(self, create, extracted, **kwargs):
        if kwargs.get("add", False) and not self.care_type == Care.EXTERNAL:
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
