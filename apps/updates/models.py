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


class FieldChange:
    def __init__(self, field, old, new, many_to_many_entity=None):
        self.field = field
        self.old = old
        self.new = new
        self.many_to_many_entity = many_to_many_entity


class ModelChange:
    def __init__(self, date, user, entity_name, entity_id, field_changes):
        self.date = date
        self.user = user
        self.entity_name = entity_name
        self.entity_id = entity_id
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
        change_list = []
        current = self.history.first()
        while current.prev_record:
            if changes := current.diff_against(current.prev_record).changes:
                change_list.append(
                    ModelChange(
                        date=current.history_date,
                        user=current.history_user,
                        field_changes=changes,
                        entity_name=self.__class__.__name__,
                        entity_id=self.id,
                    )
                )
            current = current.prev_record
        change_list.extend(self._get_m2m_changes())
        change_list.sort(key=lambda x: x.date, reverse=True)
        return change_list

    def _get_m2m_changes(self):
        changes = []
        for field in self._meta.many_to_many:
            through = getattr(self, field.name).through
            history = through.log.filter(**{f"{self._meta.model_name}_id": self})
            field_changes = self._m2m_history_to_value_changes(
                history, field.m2m_reverse_field_name()
            )
            for change in field_changes:
                changes.append(
                    ModelChange(
                        date=change["date"],
                        user=change["user"],
                        entity_name=self.__class__.__name__,
                        entity_id=self.id,
                        field_changes=[
                            FieldChange(
                                field=field.name,
                                old=change["old"],
                                new=change["new"],
                                many_to_many_entity=field.related_model._meta.object_name,
                            )
                        ],
                    )
                )
        return changes

    @staticmethod
    def _m2m_history_to_value_changes(history, reverse_field_name):
        """
        Convert m2m history to value changes
        :param history: QuerySet of HistoryRecord for many-to-many field
        :return: dictionary of value changes in format::

        {
            "date": change datetime,
            "user": change user,
            "old": list of old many-to-many values,
            "new": list of new many-to-many values,
        }

        """
        changes = []
        values = set()
        for history_record in history.order_by("history_id"):
            old_values = values.copy()
            if history_record.history_type in ["~", "+"]:
                values.add(getattr(history_record, reverse_field_name))
            elif history_record.history_type == "-":
                values.remove(getattr(history_record, reverse_field_name))
            new_values = values.copy()

            if old_values != new_values:
                changes.append(
                    {
                        "date": history_record.history_date,
                        "user": history_record.history_user,
                        "old": [v.serialize().data for v in old_values],
                        "new": [v.serialize().data for v in new_values],
                    }
                )

        return changes
