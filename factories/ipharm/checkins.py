import random

import factory

from factories.references.drugs import DrugFactory


class CheckInFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "ipharm.CheckIn"
        django_get_or_create = ["care"]

    care = factory.SubFactory("factories.ipharm.CareFactory")
    polypharmacy = factory.Faker("boolean", chance_of_getting_true=20)
    polypharmacy_note = factory.Maybe(
        "polypharmacy",
        yes_declaration=factory.Faker("text", locale="la"),
        no_declaration="",
    )
    high_interaction_potential = factory.Faker("boolean", chance_of_getting_true=20)
    high_interaction_potential_drugs = factory.Maybe(
        "high_interaction_potential",
        yes_declaration=factory.Faker("text", locale="la"),
        no_declaration="",
    )
    renal_insufficiency = factory.Faker("boolean", chance_of_getting_true=20)
    renal_insufficiency_note = factory.Maybe(
        "renal_insufficiency",
        yes_declaration=factory.Faker("text", locale="la"),
        no_declaration="",
    )
    significant_biochemical_changes = factory.Faker(
        "boolean", chance_of_getting_true=20
    )
    significant_biochemical_changes_note = factory.Maybe(
        "significant_biochemical_changes",
        yes_declaration=factory.Faker("text", locale="la"),
        no_declaration="",
    )
    systemic_corticosteroids = factory.Faker("boolean", chance_of_getting_true=20)
    systemic_corticosteroids_note = factory.Maybe(
        "systemic_corticosteroids",
        yes_declaration=factory.Faker("text", locale="la"),
        no_declaration="",
    )

    narrow_therapeutic_window = factory.Faker("boolean", chance_of_getting_true=20)
    narrow_therapeutic_window_note = factory.Maybe(
        "narrow_therapeutic_window",
        yes_declaration=factory.Faker("text", locale="la"),
        no_declaration="",
    )
    hepatic_insufficiency = factory.Faker("boolean", chance_of_getting_true=20)
    hepatic_insufficiency_note = factory.Maybe(
        "hepatic_insufficiency",
        yes_declaration=factory.Faker("text", locale="la"),
        no_declaration="",
    )
    intensive_care = factory.Faker("boolean", chance_of_getting_true=20)
    intensive_care_note = factory.Maybe(
        "intensive_care",
        yes_declaration=factory.Faker("text", locale="la"),
        no_declaration="",
    )
    pharmacist_intervention_required = factory.Faker(
        "boolean", chance_of_getting_true=20
    )
    consultation_requested = factory.Faker("boolean", chance_of_getting_true=20)
    patient_condition_change = factory.Faker("boolean", chance_of_getting_true=20)
    risk_level = factory.Iterator(["1", "2", "3"])
    created_at = factory.Faker("date_time_this_year", before_now=True, tzinfo=None)
    updated_at = factory.LazyAttribute(lambda o: o.created_at)
    medical_procedure = None

    @factory.post_generation
    def drugs(self, create, extracted, **kwargs):
        if create:
            for _ in range(random.randint(1, 4)):
                self.drugs.add(DrugFactory())

    @factory.post_generation
    def high_interaction_potential_drugs(self, create, extracted, **kwargs):
        if create:
            for _ in range(random.randint(1, 3)):
                self.high_interaction_potential_drugs.add(DrugFactory())

    @factory.post_generation
    def narrow_therapeutic_window_drugs(self, create, extracted, **kwargs):
        if create:
            for _ in range(random.randint(1, 3)):
                self.narrow_therapeutic_window_drugs.add(DrugFactory())
