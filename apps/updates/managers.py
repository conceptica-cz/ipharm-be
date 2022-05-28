import logging
from typing import Any, Callable, Iterable, List, Optional, Tuple

from common.managers import BaseSoftDeletableManager
from django.conf import settings
from django.db.models import Manager

logger = logging.getLogger(__name__)


class BaseUpdatableManager(BaseSoftDeletableManager):
    """Base manager for an updatable Model"""

    CREATED = "created"
    UPDATED = "updated"
    NOT_CHANGED = "not_changed"

    def update_or_create_from_dict(
        self,
        data: dict,
        identifiers: Iterable[str],
        relations: dict = None,
        update: "ReferenceUpdate" = None,
    ) -> [Tuple[Any, str]]:
        """Create or update model instance from data dictionary

        :param data: model values dictionary
        :param identifiers: list or tuple of unique (together) model's field, used to find existing instance
        :param relations: dictionary of relation
        :return: tuple (object, operation), where operation is one of 'created', 'updated', 'not_changed'
        """
        data = data.copy()
        logger.debug(f"Adding record", extra={"data": data})

        obj, is_changed = self._is_changed(data, relations)
        if not is_changed:
            return obj, self.NOT_CHANGED

        kwargs = {identifier: data.pop(identifier) for identifier in identifiers}
        data = self._get_relations(data, relations)
        obj, created = self.update_or_create(**kwargs, defaults=data)
        operation = self.CREATED if created else self.UPDATED
        if update:
            obj.set_update(update)
        return obj, operation

    def _is_changed(self, data: dict, relations: dict) -> Tuple[Optional[Any], bool]:
        """
        Check if model instance is changed
        :param data: dictionary of model values
        :param relations: dictionary of relation
        :return:
        """
        """Return object if one is not changed"""
        changed = False
        fields = data.copy()
        if relations is not None:
            for data_field in relations:
                field_name = relations[data_field]["field"]
                key = relations[data_field].get("key", data_field)
                field = self.model._meta.get_field(field_name)
                if field.many_to_one:
                    try:
                        related_instance = field.related_model.objects.get(
                            **{key: fields[data_field]}
                        )
                    except field.related_model.DoesNotExist:
                        return None, True
                    if relations[data_field].get("delete_source_field"):
                        del fields[data_field]
                    fields[field_name] = related_instance
        try:
            not_changed_obj = self.get(**fields)
        except self.model.DoesNotExist:
            return None, True
        else:
            return not_changed_obj, False

    def _get_relations(self, data: dict, relations: dict = None) -> dict:
        """
        Create temporary relations for model instance

        """
        if relations is None:
            return data

        for data_field in relations:
            field_name = relations[data_field]["field"]
            key = relations[data_field].get("key", data_field)
            field = self.model._meta.get_field(field_name)
            if field.many_to_one:
                if data[data_field] is None:
                    related_model = None
                else:
                    (
                        related_model,
                        _,
                    ) = field.related_model.objects.get_or_create_temporary(
                        **{key: data[data_field]}
                    )
                if relations[data_field].get("delete_source_field"):
                    del data[data_field]
                data[field_name] = related_model
        return data


class BaseTemporaryCreatableManager(BaseUpdatableManager):
    TEMPORARY_DEFAULTS = {}

    def get_temporary_defaults(self, **kwargs) -> dict:
        return self.TEMPORARY_DEFAULTS

    def get_or_create_temporary(self, **kwargs) -> Tuple[Any, bool]:
        """
        Get or create temporary instance.

        Defaults for temporary model are defined in TEMPORARY_DEFAULTS.
        """
        defaults = self.get_temporary_defaults(**kwargs)
        logger.debug(
            f"Getting or creating temporary instance {self.model} kwargs={kwargs} defaults={defaults}"
        )
        return self.get_or_create(**kwargs, defaults=defaults)


class SourceManager(Manager):
    def get_or_create_from_settings(self, name):
        source, _ = self.get_or_create(name=name)
        return source


class UpdateManager(BaseTemporaryCreatableManager):
    def delete_old_empty_updates(self):
        self.get_old_empty_updates().delete()


class ModelUpdateManager(BaseTemporaryCreatableManager):
    def delete_old_empty_updates(self):
        self.get_old_empty_updates().delete()
