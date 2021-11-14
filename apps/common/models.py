from common.managers import BaseSoftDeletableManager
from django.db import models
from simple_history.models import HistoricalRecords


class BaseSoftDeletableModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using, keep_parents)

    objects = BaseSoftDeletableManager()
    all_objects = BaseSoftDeletableManager(alive_only=False)


class BaseHistoricalModel(BaseSoftDeletableModel):
    log = HistoricalRecords(inherit=True, related_name="history")

    class Meta:
        abstract = True
