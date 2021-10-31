import logging
from typing import Any, Callable, Iterable, Tuple

from django.conf import settings
from django.db.models import Manager

logger = logging.getLogger(__name__)


class BaseUpdatableManager(Manager):
    """Base manager for an updatable Model"""

    CREATED = "created"
    UPDATED = "updated"
    NOT_CHANGED = "not_changed"

    def update_or_create_from_dict(
        self,
        identifiers: Iterable[str],
        data: dict,
        transformer: Callable[[dict], dict] = None,
        user: "User" = None,
        update: "ReferenceUpdate" = None,
    ) -> [Tuple[Any, str]]:
        """Create or update model instance from data dictionary

        :param identifiers: list or tuple of unique (together) model's field, used to find existing instance
        :param data: model values dictionary
        :param transformer: function to transform data dict
        :return: tuple (object, operation), where operaiton is one of 'created', 'updated', 'not_changed'
        """
        if transformer is not None:
            data = transformer(data)
        try:
            not_changed_obj = self.get(**data)
        except self.model.DoesNotExist:
            pass
        else:
            return not_changed_obj, self.NOT_CHANGED
        kwargs = {identifier: data.pop(identifier) for identifier in identifiers}
        obj, created = self.update_or_create(**kwargs, defaults=data)
        operation = self.CREATED if created else self.UPDATED
        if user is not None or update is not None:
            history = obj.history.first()
            history.history_user = user
            history.update = update
            history.save()
        return obj, operation


class ReferenceManager(Manager):
    def get_or_create_from_settings(self, model_name):
        name = settings.REFERENCES[model_name]["name"]
        reference, _ = self.get_or_create(model=model_name, defaults={"name": name})
        return reference
