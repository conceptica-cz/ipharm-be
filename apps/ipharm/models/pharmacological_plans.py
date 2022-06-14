from django.db import models
from django.utils import timezone
from references.models import MedicalProcedure
from updates.models import BaseUpdatableModel


class PharmacologicalPlan_tags(BaseUpdatableModel):
    pharmacologicalplan = models.ForeignKey(
        "ipharm.PharmacologicalPlan", on_delete=models.CASCADE
    )
    tag = models.ForeignKey("references.Tag", on_delete=models.CASCADE)


class PharmacologicalPlan(BaseUpdatableModel):
    care = models.OneToOneField("ipharm.Care", on_delete=models.CASCADE)
    text = models.TextField(
        blank=True, null=True, help_text="Text farmakologického plánu"
    )
    his_text = models.TextField(blank=True, null=True, help_text="UNIS text")
    note = models.TextField(blank=True, null=True, help_text="Poznámka")
    notification_datetime = models.DateTimeField(
        blank=True, null=True, help_text="Datum pro upozornění"
    )
    tags = models.ManyToManyField(
        "references.Tag",
        through=PharmacologicalPlan_tags,
        blank=True,
        help_text="Štítky",
    )
    medical_procedure = models.ForeignKey(
        "references.MedicalProcedure",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.medical_procedure:
            medical_procedure, _ = MedicalProcedure.objects.get_or_create(code="05753")
            self.medical_procedure = medical_procedure
        super(PharmacologicalPlan, self).save()


class VerificationNumberLimitIsReached(Exception):
    pass


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
    medical_procedure = models.ForeignKey(
        "references.MedicalProcedure",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    author = models.ForeignKey(
        "users.User", null=True, blank=True, on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        if self.pk is None and self.comment_type == self.VERIFICATION and self.verify:
            if (
                PharmacologicalPlanComment.objects.filter(
                    pharmacological_plan=self.pharmacological_plan,
                    comment_type=self.VERIFICATION,
                ).count()
                >= 2
            ):
                raise VerificationNumberLimitIsReached(
                    "Only two verification comments are allowed"
                )
            if not self.medical_procedure:
                medical_procedure, _ = MedicalProcedure.objects.get_or_create(
                    code="05755"
                )
            self.medical_procedure = medical_procedure
        super(PharmacologicalPlanComment, self).save()

    @property
    def care(self):
        return self.pharmacological_plan.care
