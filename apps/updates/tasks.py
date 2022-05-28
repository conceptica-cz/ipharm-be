import logging
from typing import Iterable, List, Tuple

from celery import shared_task
from requisitions.models import Requisition
from updates.bulovka.loaders import ExternalReferenceError
from updates.models import ModelUpdate, Source, Update
from updates.requisitions.updaters import update_remote_requisition
from updates.services import finish_update
from updates.utils import get_function_by_name

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
    logger.info("Task update has been started.", extra={"task_id": self.request.id})

    source = Source.objects.get_or_create_from_settings(name=source_name)
    source.update(full_update=full_update, **kwargs)

    logger.info(
        "Task update has been finished.",
        extra={"task_id": self.request.id, "source_name": source_name},
    )


@shared_task(
    bind=True,
    ignore_result=False,
    max_retries=1,
)
def task_model_updater(self, updater: str, data: dict, **kwargs):
    """Invoke model updater"""
    logger.debug(
        "Task task_model_updater has been started",
        extra={
            "task_id": self.request.id,
            "data": data,
        },
    )
    updater = get_function_by_name(updater)
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
def task_finish_update(self, update_results: List[dict], update_id: int):
    logger.info(
        "Task task_finish_update has been started",
        extra={
            "task_id": self.request.id,
            "update_results": update_results,
            "update_id": update_id,
        },
    )

    model_updates = finish_update(update_results, update_id)

    for model_update in model_updates:
        logger.info(
            "Task task_finish_update has been finished",
            extra={
                "task_id": self.request.id,
                "model": model_update.name,
                "instance_created": model_update.created,
                "instance_updated": model_update.updated,
                "instance_not_changed": model_update.not_changed,
            },
        )

    logger.info(
        "Task task_finish_update has been finished",
        extra={
            "task_id": self.request.id,
            "update_result_count": len(update_results),
            "update_id": update_id,
        },
    )


@shared_task(
    bind=True,
    ignore_result=False,
    max_retries=1,
)
def task_post_operation(self, post_operation: str, transformed_data: dict, **kwargs):
    """Invoke post_operation"""
    logger.debug(
        "Task task_post_operation has been started",
        extra={
            "task_id": self.request.id,
        },
    )
    post_operation = get_function_by_name(post_operation)
    try:
        post_operation(transformed_data, **kwargs)
    except Exception as e:
        logger.exception(e)
        return
    logger.debug(
        "Task task_post_operation has been finished",
        extra={
            "task_id": self.request.id,
        },
    )


@shared_task(
    bind=True,
    ignore_result=False,
    max_retries=1,
)
def task_update_remote_requisition(
    self, requisition_id: int, fields_to_update=Iterable[str]
):
    """Invoke update_remote_requisition"""
    logger.debug(
        "Task task_update_remote_requisition has been started",
        extra={
            "task_id": self.request.id,
            "requisition_id": requisition_id,
            "fields_to_update": fields_to_update,
        },
    )

    requisition = Requisition.objects.get(id=requisition_id)

    update_remote_requisition(requisition, fields_to_update)
    logger.debug(
        "Task task_update_remote_requisition has been finished",
        extra={
            "task_id": self.request.id,
            "requisition_id": requisition_id,
            "fields_to_update": fields_to_update,
        },
    )


@shared_task(
    bind=True,
)
def task_delete_old_emtpy_updates(self):
    logger.info(
        "Task task_delete_old_emtpy_updates has been started",
        extra={"task_id": self.request.id},
    )
    old_empty_model_updates = ModelUpdate.objects.get_old_empty_updates()
    model_update_count = old_empty_model_updates.count()
    old_empty_model_updates.delete()

    old_empty_updates = Update.objects.get_old_empty_updates()
    update_count = old_empty_updates.count()
    old_empty_updates.delete()

    logger.info(
        "Task task_delete_old_emtpy_updates has been finished",
        extra={
            "task_id": self.request.id,
            "model_update_count": model_update_count,
            "update_count": update_count,
        },
    )
