import importlib
import logging
from typing import TYPE_CHECKING, Callable, Iterable, Optional

from celery import chord
from django.conf import settings

from .tasks import task_finish_update, task_model_updater

if TYPE_CHECKING:
    from .models import Update

logger = logging.getLogger(__name__)


class UpdateError(Exception):
    pass


class Updater:
    def __init__(
        self,
        update_model: "Update",
        data_loader: Callable,
        data_loader_kwargs: dict,
        model_updater: Callable,
        model_updater_kwargs: dict,
        transformers: Optional[Iterable[Callable]] = None,
        post_operations: Optional[Iterable[Callable]] = None,
        **kwargs,
    ):
        kwargs["update_id"] = update_model.id
        self.data_loader = data_loader
        self.data_loader_kwargs = data_loader_kwargs | kwargs
        if transformers is None:
            transformers = []
        self.transformers = transformers
        if post_operations is None:
            post_operations = []
        self.post_operations = post_operations
        self.model_updater = model_updater
        self.model_updater_kwargs = model_updater_kwargs | kwargs
        self.kwargs = kwargs
        self.update_model = update_model

    def update(self):
        data = self.data_loader(**self.data_loader_kwargs)
        transformed_data = []
        for entity in data:
            try:
                for transformer in self.transformers:
                    entity = transformer(entity)
            except Exception:
                logger.exception(f"Error updating {entity}")
                continue
            else:
                transformed_data.append(entity)
        chord(
            (
                task_model_updater.s(
                    updater=self.model_updater, data=entity, **self.model_updater_kwargs
                )
                for entity in transformed_data
            ),
            task_finish_update.s(self.update_model.id),
        ).apply_async()

        for post_operation in self.post_operations:
            post_operation(transformed_data, **self.kwargs)


class UpdaterFactory:
    @staticmethod
    def _get_func(dotted_path: str) -> Callable:
        module_name, func_name = dotted_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, func_name)

    @staticmethod
    def create(source: str, update_model: "Update", **kwargs) -> Updater:
        data_loader = UpdaterFactory._get_func(
            settings.UPDATE_SOURCES[source].get(
                "data_loader", settings.DEFAULT_DATA_LOADER
            )
        )
        data_loader_kwargs = settings.UPDATE_SOURCES[source].get(
            "data_loader_kwargs", {}
        )
        model_updater = UpdaterFactory._get_func(
            settings.UPDATE_SOURCES[source].get(
                "model_updater", settings.DEFAULT_MODEL_UPDATER
            )
        )
        model_updater_kwargs = settings.UPDATE_SOURCES[source].get(
            "model_updater_kwargs", {}
        )
        transformers = [
            UpdaterFactory._get_func(transformer)
            for transformer in settings.UPDATE_SOURCES[source].get("transformers", [])
        ]
        post_operations = [
            UpdaterFactory._get_func(post_operation)
            for post_operation in settings.UPDATE_SOURCES[source].get(
                "post_operations", []
            )
        ]
        return Updater(
            update_model=update_model,
            data_loader=data_loader,
            data_loader_kwargs=data_loader_kwargs,
            model_updater=model_updater,
            model_updater_kwargs=model_updater_kwargs,
            transformers=transformers,
            post_operations=post_operations,
            **kwargs,
        )
