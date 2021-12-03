from django.db import models
from ipharm.models import Care
from references.models import Diagnosis, Drug, Tag
from updates.models import BaseUpdatableModel


class RiskDrugHistory(BaseUpdatableModel):
    care = models.OneToOneField(Care, on_delete=models.CASCADE)
    has_risk_drug = models.BooleanField(default=False, help_text="Rizikové léčivo")
    risk_drugs = models.ManyToManyField(Drug, blank=True, help_text="Seznam léčiv")
    has_risk_diagnosis = models.BooleanField(
        default=False, help_text="Riziková diagnóza"
    )
    risk_diagnoses = models.ManyToManyField(
        Diagnosis, blank=True, help_text="Seznam diagnóz"
    )
    tags = models.ManyToManyField(Tag, blank=True, help_text="Štítky")

    class Meta:
        verbose_name_plural = "Risk drug histories"


class RiskDrugHistoryComment(BaseUpdatableModel):
    risk_drug_history = models.ForeignKey(
        RiskDrugHistory, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField(help_text="Komentář")
