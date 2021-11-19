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
        identifiers: Iterable[str],
        data: dict,
        transformer: Callable[[dict], dict] = None,
        relations: dict = None,
        user: "User" = None,
        update: "ReferenceUpdate" = None,
    ) -> [Tuple[Any, str]]:
        """Create or update model instance from data dictionary

        :param identifiers: list or tuple of unique (together) model's field, used to find existing instance
        :param data: model values dictionary
        :param transformer: function to transform data dict
        :param relations: dictionary of relation
        :return: tuple (object, operation), where operation is one of 'created', 'updated', 'not_changed'
        """
        logger.debug(f"Adding record data={data}", extra={"data": data})
        if transformer is not None:
            data = transformer(data)

        obj, is_changed = self._is_changed(data, relations)
        if not is_changed:
            return obj, self.NOT_CHANGED

        kwargs = {identifier: data.pop(identifier) for identifier in identifiers}
        data, m2m_fields = self._get_relations(data, relations)
        obj, created = self.update_or_create(**kwargs, defaults=data)
        if m2m_fields:
            self._update_m2m_fields(obj, data, m2m_fields)
        operation = self.CREATED if created else self.UPDATED
        self._update_history(obj, user, update)
        return obj, operation

    def _update_m2m_fields(self, obj, data, m2m_fields):
        """Update m2m fields"""
        for field_name, related_model in m2m_fields:
            getattr(obj, field_name).remove(
                *list(getattr(obj, field_name).only_via_api())
            )
            getattr(obj, field_name).add(related_model)

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
        m2m_fields = []
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
                elif field.many_to_many:
                    try:
                        related_instance = field.related_model.objects.get(
                            **{key: fields[data_field]}
                        )
                    except field.related_model.DoesNotExist:
                        return None, True
                    else:
                        del fields[data_field]
                        m2m_fields.append((field_name, related_instance))
        try:
            not_changed_obj = self.get(**fields)
        except self.model.DoesNotExist:
            return None, True
        else:
            for m2m_field, related_instance in m2m_fields:
                if related_instance not in getattr(not_changed_obj, m2m_field).all():
                    return None, True
            return not_changed_obj, False

    @staticmethod
    def _update_history(obj, user, update):
        """Update object history"""
        if user is not None or update is not None:
            history = obj.history.first()
            history.history_user = user
            history.update = update
            history.save()

    def _get_relations(
        self, data: dict, relations: dict = None
    ) -> Tuple[dict, List[Tuple[str, Any]]]:
        """
        Create temporary relations for model instance

        """
        if relations is None:
            return data, []

        m2m_fields = []
        for data_field in relations:
            field_name = relations[data_field]["field"]
            key = relations[data_field].get("key", data_field)
            field = self.model._meta.get_field(field_name)
            if field.many_to_one:
                related_model, _ = field.related_model.objects.get_or_create_temporary(
                    **{key: data[data_field]}
                )
                if relations[data_field].get("delete_source_field"):
                    del data[data_field]
                data[field_name] = related_model
            elif field.many_to_many:
                related_model, _ = field.related_model.objects.get_or_create_temporary(
                    **{key: data.pop(data_field)}
                )
                m2m_fields.append((field_name, related_model))
        return data, m2m_fields


class BaseTemporaryCreatableManager(BaseUpdatableManager):
    TEMPORARY_DEFAULTS = {}

    def get_or_create_temporary(self, **kwargs) -> Tuple[Any, bool]:
        """
        Get or create temporary instance.

        Defaults for temporary model are defined in TEMPORARY_DEFAULTS.
        """
        defaults = self.TEMPORARY_DEFAULTS
        logger.debug(
            f"Getting or creating temporary instance {self.model} kwargs={kwargs} defaults={defaults}"
        )
        return self.get_or_create(**kwargs, defaults=defaults)


class ReferenceManager(Manager):
    def get_or_create_from_settings(self, model_name):
        name = settings.REFERENCES[model_name]["name"]
        reference, _ = self.get_or_create(model=model_name, defaults={"name": name})
        return reference
