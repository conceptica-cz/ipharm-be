from django.db import models
from ipharm.models import Care
from references.models import Tag
from updates.models import BaseUpdatableModel


class PharmacologicalPlan(BaseUpdatableModel):
    care = models.OneToOneField(Care, on_delete=models.CASCADE)
    text = models.TextField(
        blank=True, null=True, help_text="Text farmakologického plánu"
    )
    his_text = models.TextField(blank=True, null=True, help_text="UNIS text")
    note = models.TextField(blank=True, null=True, help_text="Poznámka")
    notification_datetime = models.DateTimeField(
        blank=True, null=True, help_text="Datum pro upozornění"
    )
    tags = models.ManyToManyField(Tag, blank=True, help_text="Štítky")


class PharmacologicalPlanComment(BaseUpdatableModel):
    COMMENT = "comment"
    VERIFICATION = "verification"
    COMMENT_TYPE_CHOICES = (
        (COMMENT, "Comment"),
        (VERIFICATION, "Verification"),
    )
    pharmacological_plan = models.ForeignKey(
        PharmacologicalPlan, on_delete=models.CASCADE
    )
    comment_type = models.CharField(
        max_length=20, choices=COMMENT_TYPE_CHOICES, default=COMMENT
    )
    text = models.TextField(blank=True, null=True, help_text="Text")
    verify = models.BooleanField(default=False, help_text="Vykázat ověření")
