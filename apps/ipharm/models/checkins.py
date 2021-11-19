from django.db import models
from ipharm.models.cares import Care
from references.models.drugs import Drug
from updates.models import BaseUpdatableModel


class CheckIn(BaseUpdatableModel):
    care = models.OneToOneField(Care, on_delete=models.CASCADE)
    drugs = models.ManyToManyField(
        Drug, verbose_name="seznam léčiv", blank=True, related_name="drug_checkins"
    )
    polypharmacy = models.BooleanField("polypragmazie", default=False)
    polypharmacy_note = models.TextField("poznámka k polypragmazii", blank=True)
    high_interaction_level = models.BooleanField("polypragmazie", default=False)
    high_interaction_level_drugs = models.ManyToManyField(
        Drug,
        verbose_name="seznam léčiv",
        blank=True,
        related_name="high_interaction_level_drug_checkins",
    )
    high_interaction_level_note = models.TextField(
        "poznámka k polypragmazii", blank=True
    )

    def __str__(self):
        return f"CheckIn {self.id} {self.care.patient}"
