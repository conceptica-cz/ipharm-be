import logging
from typing import Callable

from celery import shared_task
from updates.bulovka.loaders import ExternalReferenceError
from updates.common.updaters import simple_model_updater

from ipharm_web.settings import DEFAULT_RETRY_DELAY

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    ignore_result=True,
    autoretry_for=(ExternalReferenceError,),
    max_retries=1,
    default_retry_delay=DEFAULT_RETRY_DELAY,
)
def update(self, source_name: str, full_update=False, **kwargs):
    """
    Update model(s) from 3rd party source.

    :param self: task instance
    :param source_name: source name
    :param full_update: if True, update all models, otherwise only changed
    :param kwargs: kwargs
    :return:
    """
    logger.info("Task update has been started. task_id: %s", self.request.id)
    from updates.models import Source

    source = Source.objects.get_or_create_from_settings(name=source_name)
    source.update(full_update=full_update, **kwargs)


@shared_task(
    bind=True,
    ignore_result=False,
    max_retries=1,
)
def task_model_updater(self, updater: Callable, data: dict, **kwargs):
    """Invoke model updater"""
    logger.debug(
        "Task task_model_updater has been started",
        extra={
            "task_id": self.request.id,
            "data": data,
        },
    )
    try:
        operations = updater(data, **kwargs)
    except Exception as e:
        logger.exception(e)
        return {}
    logger.debug(
        "Task task_model_updater has been finished",
        extra={
            "task_id": self.request.id,
            "operations": operations,
        },
    )
    return operations


@shared_task(
    bind=True,
    ignore_result=False,
    max_retries=1,
)
def task_finish_update(self, update_results: dict, update_id: int):
    logger.debug(
        "Task task_finish_update has been started",
        extra={
            "task_id": self.request.id,
            "update_results": update_results,
            "update_id": update_id,
        },
    )
    from .services import finish_update

    finish_update(update_results, update_id)
    logger.debug(
        "Task task_finish_update has been finished",
        extra={
            "task_id": self.request.id,
            "update_results": update_results,
            "update_id": update_id,
        },
    )
