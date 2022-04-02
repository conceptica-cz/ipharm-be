from typing import List

from common.models import BaseHistoricalModel, BaseSoftDeletableModel
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from users.models import User

from .managers import BaseUpdatableManager, SourceManager
from .updater import UpdaterFactory


class Source(BaseHistoricalModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    objects = SourceManager()

    def __str__(self):
        return self.name

    def update(self, full_update=False, **kwargs):
        if full_update:
            update_type = Update.FULL
            latest_update = None
        else:
            try:
                latest_update = Update.objects.filter(source=self).latest("started_at")
            except Update.DoesNotExist:
                update_type = Update.FULL
                latest_update = None
            else:
                update_type = Update.INCREMENTAL

        update = Update.objects.create(
            source=self,
            update_type=update_type,
            started_at=timezone.now(),
            url_parameters=kwargs.get("url_parameters"),
        )
        updater = UpdaterFactory.create(
            self.name, update=update, latest_update=latest_update, **kwargs
        )
        update_result = updater.update()
        update.finish_update(update_result)


class Update(BaseHistoricalModel):
    FULL = "full"
    INCREMENTAL = "incremental"
    UPDATE_TYPES = (
        (FULL, "Full"),
        (INCREMENTAL, "Incremental"),
    )
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    update_type = models.CharField(max_length=11, choices=UPDATE_TYPES, default=FULL)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    url_parameters = models.JSONField(null=True, blank=True)

    def finish_update(self, update_result):
        self.finished_at = timezone.now()
        self.save()
        for model, model_result in update_result.items():
            ModelUpdate.objects.create(
                update=self,
                name=model,
                created=model_result.get("created", 0),
                updated=model_result.get("updated", 0),
                not_changed=model_result.get("not_changed", 0),
            )


class ModelUpdate(BaseHistoricalModel):
    update = models.ForeignKey(Update, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    created = models.IntegerField(default=0)
    updated = models.IntegerField(default=0)
    not_changed = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class UpdateHistoricalModel(models.Model):
    update = models.ForeignKey(Update, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class ModelChange:
    def __init__(self, date, user, field_changes):
        self.date = date
        self.user = user
        self.field_changes = field_changes


class BaseUpdatableModel(BaseSoftDeletableModel):
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

    def set_update(self, update: "updates.Update"):
        user = User.objects.get_updater_user()
        history = self.history.first()
        history.history_user = user
        history.update = update
        history.save()

    def set_history_user(self, user):
        history = self.history.first()
        history.history_user = user
        history.save()

    def get_changes(self):
        current = self.history.first()
        while current.prev_record:
            if changes := current.diff_against(current.prev_record).changes:
                yield ModelChange(
                    date=current.history_date,
                    user=current.history_user,
                    field_changes=changes,
                )
            current = current.prev_record
