from django.db import models
from django.utils import timezone
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
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class PharmacologicalPlanComment(BaseUpdatableModel):
    COMMENT = "comment"
    VERIFICATION = "verification"
    COMMENT_TYPE_CHOICES = (
        (COMMENT, "Comment"),
        (VERIFICATION, "Verification"),
    )
    pharmacological_plan = models.ForeignKey(
        PharmacologicalPlan, on_delete=models.CASCADE, related_name="comments"
    )
    comment_type = models.CharField(
        max_length=20, choices=COMMENT_TYPE_CHOICES, default=COMMENT
    )
    text = models.TextField(blank=True, null=True, help_text="Text")
    verify = models.BooleanField(default=False, help_text="Vykázat ověření")
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
