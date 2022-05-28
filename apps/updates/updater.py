import importlib
import logging
from typing import TYPE_CHECKING, Callable, Iterable, Optional

from celery import chain, chord
from django.conf import settings

from .utils import get_function_by_name

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
        queue: str = None,
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
        if queue is None:
            queue = settings.CELERY_TASK_DEFAULT_QUEUE
        self.queue = queue

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

        from .tasks import task_finish_update, task_model_updater, task_post_operation

        update_chord = chord(
            (
                task_model_updater.s(
                    updater=self.model_updater.__module__
                    + "."
                    + self.model_updater.__name__,
                    data=entity,
                    **self.model_updater_kwargs,
                )
                for entity in transformed_data
            ),
            task_finish_update.s(self.update_model.id),
        )

        post_operations_chain = chain(
            *(
                task_post_operation.si(
                    post_operation=post_operation.__module__
                    + "."
                    + post_operation.__name__,
                    transformed_data=transformed_data,
                    **self.kwargs,
                )
                for post_operation in self.post_operations
            )
        )

        chain(update_chord, post_operations_chain).apply_async(queue=self.queue)


class UpdaterFactory:
    @staticmethod
    def create(source: str, update_model: "Update", **kwargs) -> Updater:
        data_loader = get_function_by_name(
            settings.UPDATE_SOURCES[source].get(
                "data_loader", settings.DEFAULT_DATA_LOADER
            )
        )
        data_loader_kwargs = settings.UPDATE_SOURCES[source].get(
            "data_loader_kwargs", {}
        )
        if not "token" in data_loader_kwargs:
            data_loader_kwargs["token"] = settings.ICISELNIKY_TOKEN
        model_updater = get_function_by_name(
            settings.UPDATE_SOURCES[source].get(
                "model_updater", settings.DEFAULT_MODEL_UPDATER
            )
        )
        model_updater_kwargs = settings.UPDATE_SOURCES[source].get(
            "model_updater_kwargs", {}
        )
        transformers = [
            get_function_by_name(transformer)
            for transformer in settings.UPDATE_SOURCES[source].get("transformers", [])
        ]
        post_operations = [
            get_function_by_name(post_operation)
            for post_operation in settings.UPDATE_SOURCES[source].get(
                "post_operations", []
            )
        ]
        queue = settings.UPDATE_SOURCES[source].get(
            "queue", settings.CELERY_TASK_DEFAULT_QUEUE
        )
        return Updater(
            update_model=update_model,
            data_loader=data_loader,
            data_loader_kwargs=data_loader_kwargs,
            model_updater=model_updater,
            model_updater_kwargs=model_updater_kwargs,
            transformers=transformers,
            post_operations=post_operations,
            queue=queue,
            **kwargs,
        )
