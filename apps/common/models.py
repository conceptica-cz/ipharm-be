from django.db import models
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        return super().delete(using, keep_parents)
