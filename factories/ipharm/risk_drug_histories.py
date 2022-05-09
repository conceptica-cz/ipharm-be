import random

import factory

from factories.ipharm import CareFactory
from factories.references import DiagnosisFactory, DrugFactory, TagFactory


class RiskDrugHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "ipharm.RiskDrugHistory"

    care = factory.SubFactory(CareFactory)
    has_risk_drug = factory.Faker("boolean", chance_of_getting_true=50)
    has_risk_diagnosis = factory.Faker("boolean", chance_of_getting_true=50)

    @factory.post_generation
    def diagnoses(self, create, extracted, **kwargs):
        if kwargs.get("add", False):
            for _ in range(random.randint(1, 4)):
                RiskDrugHistoryDiagnosisFactory(risk_drug_history=self, drugs__add=True)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if create:
            for _ in range(random.randint(1, 4)):
                self.tags.add(TagFactory())

    @factory.post_generation
    def comments(self, create, extracted, **kwargs):
        [
            RiskDrugHistoryCommentFactory(risk_drug_history=self)
            for i in range(random.randint(1, 3))
        ]


class RiskDrugHistoryDiagnosisFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "ipharm.RiskDrugHistoryDiagnosis"
        django_get_or_create = ["risk_drug_history", "diagnosis"]

    risk_drug_history = factory.SubFactory("factories.ipharm.RiskDrugHistoryFactory")
    diagnosis = factory.SubFactory("factories.references.DiagnosisFactory")

    @factory.post_generation
    def drugs(self, create, extracted, **kwargs):
        if kwargs.get("add", False):
            for _ in range(random.randint(1, 4)):
                self.drugs.add(DrugFactory())


class RiskDrugHistoryCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "ipharm.RiskDrugHistoryComment"

    risk_drug_history = factory.SubFactory(RiskDrugHistoryFactory)
    text = factory.Faker("text", locale="la")
