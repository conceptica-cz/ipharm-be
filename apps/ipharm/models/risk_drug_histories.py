from django.db import models
from django.utils import timezone
from updates.models import BaseUpdatableModel


class RiskDrugHistory_risk_drugs(BaseUpdatableModel):
    riskdrughistory = models.ForeignKey(
        "ipharm.RiskDrugHistory", on_delete=models.CASCADE
    )
    drug = models.ForeignKey("references.Drug", on_delete=models.CASCADE)


class RiskDrugHistory_risk_diagnoses(BaseUpdatableModel):
    riskdrughistory = models.ForeignKey(
        "ipharm.RiskDrugHistory", on_delete=models.CASCADE
    )
    diagnosis = models.ForeignKey("references.Diagnosis", on_delete=models.CASCADE)


class RiskDrugHistory_tags(BaseUpdatableModel):
    riskdrughistory = models.ForeignKey(
        "ipharm.RiskDrugHistory", on_delete=models.CASCADE
    )
    tag = models.ForeignKey("references.Tag", on_delete=models.CASCADE)


class RiskDrugHistory(BaseUpdatableModel):
    care = models.OneToOneField("ipharm.Care", on_delete=models.CASCADE)
    has_risk_drug = models.BooleanField(default=False, help_text="Rizikové léčivo")
    risk_drugs = models.ManyToManyField(
        "references.Drug",
        through=RiskDrugHistory_risk_drugs,
        blank=True,
        help_text="Seznam léčiv",
    )
    has_risk_diagnosis = models.BooleanField(
        default=False, help_text="Riziková diagnóza"
    )
    risk_diagnoses = models.ManyToManyField(
        "references.Diagnosis",
        through=RiskDrugHistory_risk_diagnoses,
        blank=True,
        help_text="Seznam diagnóz",
    )
    tags = models.ManyToManyField(
        "references.Tag", through=RiskDrugHistory_tags, blank=True, help_text="Štítky"
    )
    note = models.TextField(blank=True, help_text="Poznámka")

    class Meta:
        verbose_name_plural = "Risk drug histories"

    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class RiskDrugHistoryComment(BaseUpdatableModel):
    risk_drug_history = models.ForeignKey(
        RiskDrugHistory, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField(help_text="Komentář")
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
