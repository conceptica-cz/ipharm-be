from django.db import models
from django.utils import timezone
from ipharm.models.cares import Care
from references.models import MedicalProcedure
from references.models.drugs import Drug
from updates.models import BaseUpdatableModel


class CheckIn_drugs(BaseUpdatableModel):
    checkin = models.ForeignKey("ipharm.CheckIn", on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)


class CheckIn_high_interaction_potential_drugs(BaseUpdatableModel):
    checkin = models.ForeignKey("ipharm.CheckIn", on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)


# class CheckIn_diagnoses(BaseUpdatableModel):
#     checkin = models.ForeignKey("ipharm.CheckIn", on_delete=models.CASCADE)
#     diagnosis = models.ForeignKey("references.Diagnosis", on_delete=models.CASCADE)
#
#
# class CheckIn_diagnoses_drugs(BaseUpdatableModel):
#     checkin = models.ForeignKey("ipharm.CheckIn", on_delete=models.CASCADE)
#     drug = models.ForeignKey(Drug, on_delete=models.CASCADE)


class CheckIn_narrow_therapeutic_window_drugs(BaseUpdatableModel):
    checkin = models.ForeignKey("ipharm.CheckIn", on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)


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
        Drug,
        through=CheckIn_drugs,
        blank=True,
        related_name="drug_checkins",
        help_text="Seznam léčiv",
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
        through=CheckIn_high_interaction_potential_drugs,
        blank=True,
        related_name="high_interaction_potential_checkins",
        help_text="Seznam léčiv s vysokým účinkovým tlakem",
    )
    high_interaction_potential_note = models.TextField(
        blank=True,
        help_text="Poznámka k léčivám s vysokým interakčním potenciálem",
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
        through=CheckIn_narrow_therapeutic_window_drugs,
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
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    medical_procedure = models.ForeignKey(
        "references.MedicalProcedure",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    toggle_diagnoses = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.medical_procedure and (
            self.patient_condition_change
            or self.risk_level in [self.RISK_LEVEL_2, self.RISK_LEVEL_3]
        ):
            medical_procedure, _ = MedicalProcedure.objects.get_or_create(code="05751")
            self.medical_procedure = medical_procedure
        super(CheckIn, self).save()


class CheckInDiagnosisDrug(BaseUpdatableModel):
    check_in_diagnosis = models.ForeignKey(
        "ipharm.CheckInDiagnosis", on_delete=models.CASCADE
    )
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)


class CheckInDiagnosis(BaseUpdatableModel):
    check_in = models.ForeignKey(
        CheckIn, on_delete=models.CASCADE, related_name="diagnoses"
    )
    diagnosis = models.ForeignKey(
        "references.Diagnosis", on_delete=models.CASCADE, help_text="Diagnóza"
    )
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    drugs = models.ManyToManyField(
        Drug,
        through=CheckInDiagnosisDrug,
        blank=True,
        related_name="check_in_diagnoses",
        help_text="Seznam léčiv diagnózy",
    )

    class Meta:
        unique_together = ("check_in", "diagnosis")
        verbose_name_plural = "CheckInDiagnoses"
