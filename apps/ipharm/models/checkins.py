from django.db import models
from ipharm.models.cares import Care
from references.models.drugs import Drug
from updates.models import BaseUpdatableModel


class CheckIn(BaseUpdatableModel):
    RISK_LEVEL_1 = "1"
    RISK_LEVEL_2 = "2"
    RISK_LEVEL_3 = "3"
    RISK_LEVEL_CHOICE = (
        (RISK_LEVEL_1, "1. stupeň"),
        (RISK_LEVEL_2, "2. stupeň"),
        (RISK_LEVEL_3, "3. stupeň"),
    )

    care = models.OneToOneField(Care, on_delete=models.CASCADE)
    drugs = models.ManyToManyField(
        Drug, blank=True, related_name="drug_checkins", help_text="Seznam léčiv"
    )
    polypharmacy = models.BooleanField(default=False, help_text="Polypragmazie")
    polypharmacy_note = models.TextField(
        "poznámka k polypragmazii", blank=True, help_text="Poznámka k polypragmazii"
    )
    high_interaction_potential = models.BooleanField(
        "polypragmazie",
        default=False,
        help_text="Léčiva s vysokým interakčním potenciálem",
    )
    high_interaction_potential_drugs = models.ManyToManyField(
        Drug,
        blank=True,
        related_name="high_interaction_potential_checkins",
        help_text="Seznam léčiv s vysokým účinkovým tlakem",
    )
    high_interaction_potential_note = models.TextField(
        blank=True,
        help_text="Poznámka k léčivám s vysokým interakčním potenciálem",
    )
    diagnoses = models.ManyToManyField(
        "references.Diagnosis",
        blank=True,
        help_text="Diagnóza",
    )
    diagnoses_drugs = models.ManyToManyField(
        Drug,
        blank=True,
        related_name="drugs_checkins",
        help_text="Seznam léčiv",
    )
    diagnoses_note = models.TextField(
        blank=True,
        help_text="Poznámka",
    )
    renal_insufficiency = models.BooleanField(
        default=False, help_text="Renální insuficience"
    )
    renal_insufficiency_note = models.TextField(
        blank=True, help_text="Poznámka k renální insuficience"
    )
    significant_biochemical_changes = models.BooleanField(
        default=False,
        help_text="Další významné změny biochemických nebo hematolologických parametrů",
    )
    significant_biochemical_changes_note = models.TextField(
        blank=True,
        help_text="Poznámka k dalším významným změnám biochemických nebo hematolologických parametrů",
    )
    systemic_corticosteroids = models.BooleanField(
        default=False,
        help_text="Systémové kortikoidy nebo jiné imunosupresiva",
    )
    systemic_corticosteroids_note = models.TextField(
        blank=True,
        help_text="Poznámka k systémovým kortikoidům nebo jiným imunosupresivům",
    )
    narrow_therapeutic_window = models.BooleanField(
        default=False,
        help_text="Léčiva s úzkým terapeutickým oknem",
    )
    narrow_therapeutic_window_drugs = models.ManyToManyField(
        Drug,
        blank=True,
        related_name="narrow_therapeutic_window_checkins",
        help_text="Seznam léčiv s úzkým terapeutickým oknem",
    )
    narrow_therapeutic_window_note = models.TextField(
        blank=True,
        help_text="Poznámka k léčivům s úzkým terapeutickým oknem",
    )
    hepatic_insufficiency = models.BooleanField(
        default=False,
        help_text="Laboratorní známky hepatální insuficience",
    )
    hepatic_insufficiency_note = models.TextField(
        blank=True,
        help_text="Poznámka k laboratorním známkám hepatální insuficience",
    )
    intensive_care = models.BooleanField(
        default=False,
        help_text="Pacient v intenzivní péči",
    )
    intensive_care_note = models.TextField(
        blank=True,
        help_text="Poznámka k intenzivní péči",
    )
    pharmacist_intervention_required = models.BooleanField(
        default=False,
        help_text="Nutný zásah klinického farmaceuta",
    )
    consultation_requested = models.BooleanField(
        default=False,
        help_text="Vyžádané konzilium",
    )

    risk_level = models.CharField(
        max_length=1,
        choices=RISK_LEVEL_CHOICE,
        default=RISK_LEVEL_1,
        help_text="Výsledný stupeň rizikovosti",
    )
    patient_condition_change = models.BooleanField(
        default=False, help_text="Změna stavu pacienta"
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    for_insurance = models.BooleanField(
        default=False,
        help_text="Používat pro vykazování pojištění",
    )
