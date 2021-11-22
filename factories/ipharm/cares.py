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

    class Params:
        finished_at_decider = factory.LazyFunction(lambda: bool(random.randint(0, 8)))

    patient = factory.SubFactory(PatientFactory)
    care_type = factory.Iterator([Care.HOSPITALIZATION, Care.AMBULATION])
    is_active = True
    main_diagnosis = factory.SubFactory(DiagnosisFactory)
    external_id = factory.Sequence(lambda n: n)

    clinic = factory.SubFactory(ClinicFactory)
    department = factory.SubFactory(DepartmentFactory)
    started_at = fuzzy.FuzzyDateTime(
        datetime.datetime(2021, 9, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2021, 10, 1, tzinfo=datetime.timezone.utc),
    )
    finished_at = factory.Maybe(
        "datetime_out_decider",
        yes_declaration=None,
        no_declaration=factory.fuzzy.FuzzyDateTime(
            datetime.datetime(2021, 10, 1, tzinfo=datetime.timezone.utc)
        ),
    )

    @factory.post_generation
    def patient_care(self, create, extracted, **kwargs):
        if create:
            if self.care_type == Care.HOSPITALIZATION:
                self.patient.current_hospital_care = self
            elif self.care_type == Care.AMBULATION:
                self.patient.current_ambulance_care = self
            self.patient.save()

    @factory.post_generation
    def dekurzes(self, create, extracted, **kwargs):
        if create:
            for _ in range(random.randint(1, 5)):
                self.add_dekurz(DekurzFactory(care=self))

    @factory.post_generation
    def diagnozes(self, create, extracted, **kwargs):
        if create:
            for _ in range(random.randint(1, 5)):
                self.diagnoses.add(DiagnosisFactory())

    @factory.post_generation
    def children(self, create, extracted, **kwargs):
        if create:
            check_in = random.randint(0, 5) > 4
            if check_in:
                from factories.ipharm import CheckInFactory

                CheckInFactory(care=self)


class DekurzFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dekurz

    care = factory.SubFactory(CareFactory)
    made_at = fuzzy.FuzzyDateTime(
        datetime.datetime(2021, 9, 1, tzinfo=datetime.timezone.utc)
    )
    doctor = factory.SubFactory(PersonFactory)
    department = factory.SubFactory(DepartmentFactory)
