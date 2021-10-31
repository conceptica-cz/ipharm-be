import importlib
import logging
from typing import Generator, List

import requests
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from updates.models import Reference, ReferenceUpdate
from users.models import User

logger = logging.getLogger(__name__)


class ReferenceSettings:
    """Class encapsulated reference settings"""

    def __init__(self, model_name: str):
        model_type = ContentType.objects.get(
            app_label="references", model=model_name.lower()
        )
        self.model_class = model_type.model_class()
        self.transformer = self._get_transformer(model_name)
        self.identifiers = settings.REFERENCES[model_name]["identifiers"]
        self.url = settings.BASE_REFERENCES_URL + settings.REFERENCES[model_name]["url"]

    @staticmethod
    def _get_transformer(model_name):
        module_name, func_name = settings.REFERENCES[model_name]["transformer"].split(
            "."
        )
        module = importlib.import_module(f"updates.{module_name}")
        return getattr(module, func_name)


def get_data(url) -> Generator[dict, None, None]:
    """Get data from 3rd-party API

    Note: it yield list of results, not results

    :param url: start url
    :return: generator yielding lists of results
    """
    # TODO extract API class
    headers = {"Authorization": f"Bearer {settings.REFERENCES_TOKEN}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    results = data["results"]
    for result in results:
        yield result
    if (next_url := data.get("next")) is not None:
        yield from get_data(url=next_url)


class Updater:
    def __init__(self, model_name):
        self.reference_settings = ReferenceSettings(model_name)
        self.reference = Reference.objects.get_or_create_from_settings(model_name)
        self.created = 0
        self.updated = 0
        self.not_changed = 0
        self.reference_update: ReferenceUpdate = None
        self.user = User.objects.get_updater_user()

    def _update_object(self, data: dict):
        model = self.reference_settings.model_class
        _, operation = model.objects.update_or_create_from_dict(
            identifiers=self.reference_settings.identifiers,
            data=data,
            transformer=self.reference_settings.transformer,
            user=self.user,
            update=self.reference_update,
        )
        if operation == model.objects.CREATED:
            self.created += 1
        elif operation == model.objects.UPDATED:
            self.updated += 1
        else:
            self.not_changed += 1

    def update(self):
        self.created = 0
        self.updated = 0
        self.not_changed = 0
        self.reference_update = self.reference.create_update()
        for obj_data in get_data(self.reference_settings.url):
            self._update_object(obj_data)
        self.reference_update.finish_update(
            created=self.created, updated=self.updated, not_changed=self.not_changed
        )
