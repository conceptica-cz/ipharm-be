from dataclasses import dataclass
from typing import Any, List

from common.models import BaseHistoricalModel, BaseSoftDeletableModel
from django.conf import settings
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from users.models import User

from .managers import (
    BaseUpdatableManager,
    ModelUpdateManager,
    SourceManager,
    UpdateManager,
)
from .querysets import ModelUpdateQuerySet, UpdateQuerySet
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
        if latest_update:
            latest_update_id = latest_update.pk
        else:
            latest_update_id = None
        updater = UpdaterFactory.create(
            self.name, update_model=update, latest_update_id=latest_update_id, **kwargs
        )
        updater.update()


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

    objects = UpdateManager.from_queryset(UpdateQuerySet)()

    def finish_update(self, update_result):
        self.finished_at = timezone.now()
        self.save()
        for model, model_result in update_result.items():
            ModelUpdate.objects.create(
                update_model=self,
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
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ModelUpdateManager.from_queryset(ModelUpdateQuerySet)()

    def __str__(self):
        return self.name


class UpdateHistoricalModel(models.Model):
    update = models.ForeignKey(Update, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


@dataclass(eq=True)
class FieldChange:
    field: str
    old: Any
    new: Any
    many_to_many_entity: str = None


@dataclass(eq=True)
class ModelChange:
    date: timezone.datetime
    user: User
    entity_name: str
    entity_id: int
    field_changes: List[FieldChange]

    def __add__(self, other):
        if self.date > other.date:
            raise ValueError("change_1 must be older than change_2")
        # user must be the same
        if self.user != other.user:
            raise ValueError("change_1 and change_2 must have the same user")

        for field_change in other.field_changes:
            try:
                source_field_change = next(
                    f for f in self.field_changes if f.field == field_change.field
                )
            except StopIteration:
                self.field_changes.append(field_change)
            else:
                source_field_change.new = field_change.new
        return self


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

    def get_changes(
        self,
        datetime_from: timezone.datetime = None,
        datetime_to: timezone.datetime = None,
    ) -> List[ModelChange]:
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

        def datetime_filter(model_change):
            if datetime_from and model_change.date < datetime_from:
                return False
            if datetime_to and model_change.date > datetime_to:
                return False
            return True

        change_list = list(filter(datetime_filter, change_list))
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
        through_values = {}
        for history_record in history.order_by("history_id"):
            old_values = values.copy()

            value = getattr(history_record, reverse_field_name)
            through_id = history_record.id
            history_type = history_record.history_type

            if history_type in ["~", "+"]:
                if through_id in through_values and history_type == "~":
                    if value != through_values[through_id]:
                        values.remove(through_values[through_id])
                through_values[through_id] = value
                values.add(value)
            elif history_type == "-":
                if value in values:
                    values.remove(value)

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

    def get_merged_changes(self, datetime_from=None, datetime_to=None):
        return self._merge_changes(self.get_changes(datetime_from, datetime_to))

    @staticmethod
    def _merge_changes(changes: list[ModelChange]):
        """
        Merge changes if interval between changes
        is less than settings.CHANGE_HISTORY_MAX_INTERVAL minute

        :param changes: list of ModelChange
        :return: list of merged changes
        """
        changes = sorted(changes, key=lambda x: x.date)

        merged_changes = []

        by_user = {}
        for change in changes:
            by_user.setdefault(change.user, []).append(change)

        for user_changes in by_user.values():

            user_merged_changes = [user_changes[0]]

            for change in user_changes[1:]:
                if change.date - user_merged_changes[-1].date <= timezone.timedelta(
                    milliseconds=settings.CHANGE_HISTORY_MAX_INTERVAL
                ):
                    user_merged_changes[-1] += change
                else:
                    user_merged_changes.append(change)

            merged_changes.extend(user_merged_changes)

        return sorted(merged_changes, key=lambda x: x.date, reverse=True)
