from django.db import models
from django.utils import timezone
from updates.models import BaseUpdatableModel


class RiskDrugHistory_tags(BaseUpdatableModel):
    riskdrughistory = models.ForeignKey(
        "ipharm.RiskDrugHistory", on_delete=models.CASCADE
    )
    tag = models.ForeignKey("references.Tag", on_delete=models.CASCADE)


class RiskDrugHistory(BaseUpdatableModel):
    care = models.OneToOneField("ipharm.Care", on_delete=models.CASCADE)
    has_risk_drug = models.BooleanField(default=False, help_text="Rizikové léčivo")
    has_risk_diagnosis = models.BooleanField(
        default=False, help_text="Riziková diagnóza"
    )
    tags = models.ManyToManyField(
        "references.Tag", through=RiskDrugHistory_tags, blank=True, help_text="Štítky"
    )
    note = models.TextField(blank=True, help_text="Poznámka")

    class Meta:
        verbose_name_plural = "Risk drug histories"

    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class RiskDrugHistoryDiagnosisDrug(BaseUpdatableModel):
    check_in_diagnosis = models.ForeignKey(
        "ipharm.RiskDrugHistoryDiagnosis", on_delete=models.CASCADE
    )
    drug = models.ForeignKey("references.Drug", on_delete=models.CASCADE)


class RiskDrugHistoryDiagnosis(BaseUpdatableModel):
    risk_drug_history = models.ForeignKey(
        RiskDrugHistory, on_delete=models.CASCADE, related_name="diagnoses"
    )
    diagnosis = models.ForeignKey(
        "references.Diagnosis", on_delete=models.CASCADE, help_text="Diagnóza"
    )
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    drugs = models.ManyToManyField(
        "references.Drug",
        through=RiskDrugHistoryDiagnosisDrug,
        blank=True,
        related_name="risk_drug_history_diagnoses",
        help_text="Seznam léčiv diagnózy",
    )

    class Meta:
        unique_together = ("risk_drug_history", "diagnosis")
        verbose_name_plural = "RiskDrugHistoryDiagnoses"


class RiskDrugHistoryComment(BaseUpdatableModel):
    risk_drug_history = models.ForeignKey(
        RiskDrugHistory, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField(help_text="Komentář")
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
