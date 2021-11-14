from common.models import BaseHistoricalModel, BaseSoftDeletableModel
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from .managers import BaseUpdatableManager, ReferenceManager


class Reference(BaseHistoricalModel):
    model = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    objects = ReferenceManager()

    def __str__(self):
        return self.model

    def create_update(self):
        return ReferenceUpdate.objects.create(reference=self, started_at=timezone.now())


class ReferenceUpdate(BaseHistoricalModel):
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    created = models.IntegerField(default=0)
    updated = models.IntegerField(default=0)
    not_changed = models.IntegerField(default=0)

    def finish_update(self, created: int, updated: int, not_changed: int):
        # TODO create test
        self.finished_at = timezone.now()
        self.created = created
        self.updated = updated
        self.not_changed = not_changed
        self.save()


class UpdateHistoricalModel(models.Model):
    update = models.ForeignKey(
        ReferenceUpdate, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        abstract = True


class BaseUpdatableModel(UpdateHistoricalModel, BaseSoftDeletableModel):
    """Base class for model, updatable via 3rd-party Rest API"""

    log = HistoricalRecords(
        bases=[
            UpdateHistoricalModel,
        ],
        inherit=True,
        related_name="history",
    )

    objects = BaseUpdatableManager()
    all_objects = BaseUpdatableManager(alive_only=False)

    class Meta:
        abstract = True
