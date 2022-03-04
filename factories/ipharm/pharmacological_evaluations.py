import random

import factory

from factories.ipharm import CareFactory
from factories.references import DrugFactory, TagFactory


class PharmacologicalEvaluationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "ipharm.PharmacologicalEvaluation"

    care = factory.SubFactory(CareFactory)
    drug = factory.SubFactory(DrugFactory)

    deployment_initial_diagnosis = factory.Faker("boolean", chance_of_getting_true=50)
    deployment_during_diagnosis = factory.Faker("boolean", chance_of_getting_true=50)
    deployment_ft_approach = factory.Faker("boolean", chance_of_getting_true=50)
    deployment_other_reason = factory.Faker("text", locale="la")

    discontinuation_contradiction = factory.Faker("boolean", chance_of_getting_true=50)
    discontinuation_adverse_effect = factory.Faker("boolean", chance_of_getting_true=50)
    discontinuation_adverse_effect_risk = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    discontinuation_missing_indication = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    discontinuation_allergies = factory.Faker("boolean", chance_of_getting_true=50)
    discontinuation_drug_interaction = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    discontinuation_duplicity = factory.Faker("boolean", chance_of_getting_true=50)
    discontinuation_renal_insufficiency = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    discontinuation_hepatic_insufficiency = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    discontinuation_medical_intervention = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    discontinuation_underdosage = factory.Faker("boolean", chance_of_getting_true=50)
    discontinuation_underdosage_risk = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    discontinuation_other_reason = factory.Faker("text", locale="la")

    dose_change_adverse_effect = factory.Faker("boolean", chance_of_getting_true=50)
    dose_change_adverse_effect_risk = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    dose_change_renal_insufficiency = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    dose_change_hepatic_insufficiency = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    dose_change_drug_interaction = factory.Faker("boolean", chance_of_getting_true=50)
    dose_change_underdosage = factory.Faker("boolean", chance_of_getting_true=50)
    dose_change_overdosage = factory.Faker("boolean", chance_of_getting_true=50)
    dose_change_laboratory_findings = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    dose_change_dosage_reduction = factory.Faker("boolean", chance_of_getting_true=50)
    dose_change_dosage_increase = factory.Faker("boolean", chance_of_getting_true=50)
    dose_change_other_reason = factory.Faker("text", locale="la")

    continuation_drug_reintroduction = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    continuation_medical_intervention = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    continuation_other_reason = factory.Faker("text", locale="la")

    tdm_interpretation = factory.Faker("boolean", chance_of_getting_true=50)
    tdm_measure_level_recommendation = factory.Faker(
        "boolean", chance_of_getting_true=50
    )

    specific_adverse_effect_diagnosis = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    specific_adverse_effect_reporting = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    specific_consultation = factory.Faker("boolean", chance_of_getting_true=50)

    recommended_investigation_by_specialist = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    recommended_investigation_by_laboratory = factory.Faker(
        "boolean", chance_of_getting_true=50
    )
    recommended_investigation_by_physical = factory.Faker(
        "boolean", chance_of_getting_true=50
    )

    dosage_determination = factory.Faker("text", locale="la")
    administration_method_optimization = factory.Faker("text", locale="la")

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if create:
            for _ in range(random.randint(0, 4)):
                self.tags.add(TagFactory())

    @factory.post_generation
    def comments(self, create, extracted, **kwargs):
        if create:
            for _ in range(random.randint(0, 4)):
                PharmacologicalEvaluationCommentFactory(pharmacological_evaluation=self)


class PharmacologicalEvaluationCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "ipharm.PharmacologicalEvaluationComment"

    pharmacological_evaluation = factory.SubFactory(PharmacologicalEvaluationFactory)
    text = factory.Faker("text", locale="la")
