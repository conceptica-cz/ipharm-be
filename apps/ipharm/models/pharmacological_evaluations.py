from django.db import models
from django.utils import timezone
from ipharm.models import Care
from references.models import Drug, Tag
from updates.models import BaseUpdatableModel


class PharmacologicalEvaluation(BaseUpdatableModel):
    care = models.ForeignKey(Care, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)

    deployment_initial_diagnosis = models.BooleanField(
        default=False, help_text="Diagnóza ve vstupní kontrole"
    )
    deployment_during_diagnosis = models.BooleanField(
        default=False, help_text="Diagnóza v průběhu hospitalizace"
    )
    deployment_ft_approach = models.BooleanField(
        default=False, help_text="Vhodnější FT přístup"
    )
    deployment_other_reason = models.TextField(
        blank=True, null=True, help_text="Jiný důvod"
    )

    discontinuation_contradiction = models.BooleanField(
        default=False, help_text="Kontraindikace"
    )
    discontinuation_adverse_effect = models.BooleanField(
        default=False, help_text="Projev nežádoucího účinku"
    )
    discontinuation_adverse_effect_risk = models.BooleanField(
        default=False, help_text="Riziko nežádoucího účinku"
    )
    discontinuation_missing_indication = models.BooleanField(
        default=False, help_text="Chybějící indikace"
    )
    discontinuation_allergies = models.BooleanField(default=False, help_text="Alergie")
    discontinuation_drug_interaction = models.BooleanField(
        default=False, help_text="Léková interakce"
    )
    discontinuation_duplicity = models.BooleanField(
        default=False, help_text="Duplicity"
    )
    discontinuation_renal_insufficiency = models.BooleanField(
        default=False, help_text="Renální insuficience"
    )
    discontinuation_hepatic_insufficiency = models.BooleanField(
        default=False, help_text="Hepatální insuficience"
    )
    discontinuation_medical_intervention = models.BooleanField(
        default=False, help_text="Lékařská intervence"
    )
    discontinuation_underdosage = models.BooleanField(
        default=False, help_text="Poddávkování"
    )
    discontinuation_underdosage_risk = models.BooleanField(
        default=False, help_text="Rizika poddávkováí"
    )
    discontinuation_other_reason = models.TextField(
        blank=True, null=True, help_text="Jiný důvod"
    )

    dose_change_adverse_effect = models.BooleanField(
        default=False, help_text="Projev nežádoucího účinku"
    )
    dose_change_adverse_effect_risk = models.BooleanField(
        default=False, help_text="Riziko nežádoucího účinku"
    )
    dose_change_renal_insufficiency = models.BooleanField(
        default=False, help_text="Hepatální insuficience"
    )
    dose_change_hepatic_insufficiency = models.BooleanField(
        default=False, help_text="Renální insuficience"
    )
    dose_change_drug_interaction = models.BooleanField(
        default=False, help_text="Léková interakce"
    )
    dose_change_underdosage = models.BooleanField(
        default=False, help_text="Poddávkování"
    )
    dose_change_overdosage = models.BooleanField(
        default=False, help_text="Předávkování"
    )
    dose_change_laboratory_findings = models.BooleanField(
        default=False, help_text="Na základě laboratorních výseldků"
    )
    dose_change_dosage_reduction = models.BooleanField(
        default=False, help_text="Snížení dávky"
    )
    dose_change_dosage_increase = models.BooleanField(
        default=False, help_text="Zvýšení dávky"
    )
    dose_change_other_reason = models.TextField(
        blank=True, null=True, help_text="Jiný důvod"
    )

    continuation_drug_reintroduction = models.BooleanField(
        default=False, help_text="Znovunasazení léčiva"
    )
    continuation_medical_intervention = models.BooleanField(
        default=False, help_text="Po lékařské intervenci"
    )
    continuation_other_reason = models.TextField(
        blank=True, null=True, help_text="Jiný důvod"
    )

    tdm_interpretation = models.BooleanField(
        default=False, help_text="TDM - Interpretace"
    )
    tdm_measure_level_recommendation = models.BooleanField(
        default=False, help_text="TDM - Doporučení změření hladiny"
    )

    specific_adverse_effect_diagnosis = models.BooleanField(
        default=False, help_text="Specifika - Diagnostika nežádoucího účinku"
    )
    specific_adverse_effect_reporting = models.BooleanField(
        default=False, help_text="Specifika - Hlášení nežádoucího účinku"
    )
    specific_consultation = models.BooleanField(
        default=False, help_text="Specifika - Konzultace"
    )

    recommended_investigation_by_specialist = models.BooleanField(
        default=False, help_text="Doporučené vyšetření - Specialistou"
    )
    recommended_investigation_by_laboratory = models.BooleanField(
        default=False, help_text="Doporučené vyšetření - Laboratoří"
    )
    recommended_investigation_by_physical = models.BooleanField(
        default=False, help_text="Doporučené vyšetření - Fyzikální"
    )

    dosage_determination = models.TextField(
        blank=True, null=True, help_text="Stanovení dávky (při zahájení terapie)"
    )
    administration_method_optimization = models.TextField(
        blank=True, null=True, help_text="Optimalizace způsobu poddání"
    )
    tags = models.ManyToManyField(Tag, blank=True, help_text="Štítky")
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
