import logging

from django.db import models
from requisitions.managers.requisitions import RequisitionManager
from updates.models import BaseUpdatableModel

logger = logging.getLogger(__name__)


class Requisition(BaseUpdatableModel):
    TYPE_IPHARM = "ipharm"
    TYPE_DELIVERY = "delivery"

    TYPE_CHOICES = (
        (TYPE_IPHARM, "ipharm"),
        (TYPE_DELIVERY, "delivery"),
    )

    SUBTYPE_IPHARM_CONCILATION = "ipharm_conciliation"
    SUBTYPE_IPHARM_ADVERSE_EFFECT = "ipahrm_adverse_effect"

    SUBTYPE_CHOICES = (
        (SUBTYPE_IPHARM_CONCILATION, "ipharm_conciliation"),
        (SUBTYPE_IPHARM_ADVERSE_EFFECT, "ipharm_adverse_effect"),
    )

    STATE_CREATED = "created"
    STATE_PENDING = "pending"
    STATE_CANCELED = "canceled"
    STATE_REFUSED = "refused"
    STATE_SOLVED = "solved"

    STATE_CHOICES = (
        (STATE_CREATED, "Created"),
        (STATE_PENDING, "Pending"),
        (STATE_CANCELED, "Canceled"),
        (STATE_REFUSED, "Refused"),
        (STATE_SOLVED, "Solved"),
    )

    external_id = models.BigIntegerField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=TYPE_IPHARM)
    subtype = models.CharField(
        max_length=50, choices=SUBTYPE_CHOICES, default=SUBTYPE_IPHARM_CONCILATION
    )

    state = models.CharField(
        max_length=255, choices=STATE_CHOICES, default=STATE_CREATED
    )
    patient = models.ForeignKey(
        "ipharm.Patient",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="requisitions",
    )
    care = models.ForeignKey(
        "ipharm.Care",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="requisitions",
    )
    text = models.TextField(blank=True, null=True)
    file_link = models.CharField(max_length=255, blank=True, null=True)
    applicant = models.ForeignKey(
        "references.Person",
        on_delete=models.CASCADE,
        related_name="applicant_requisitions",
    )
    solver = models.ForeignKey(
        "references.Person",
        on_delete=models.CASCADE,
        related_name="solver_requisitions",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_synced = models.BooleanField(default=False)
    synced_at = models.DateTimeField(blank=True, null=True)

    objects = RequisitionManager()
