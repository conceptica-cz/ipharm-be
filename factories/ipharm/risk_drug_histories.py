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
    def risk_drugs(self, create, extracted, **kwargs):
        if create:
            for _ in range(random.randint(1, 4)):
                self.risk_drugs.add(DrugFactory())

    @factory.post_generation
    def risk_diagnoses(self, create, extracted, **kwargs):
        if create:
            for _ in range(random.randint(1, 4)):
                self.risk_diagnoses.add(DiagnosisFactory())

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


class RiskDrugHistoryCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "ipharm.RiskDrugHistoryComment"

    risk_drug_history = factory.SubFactory(RiskDrugHistoryFactory)
    text = factory.Faker("text", locale="la")
