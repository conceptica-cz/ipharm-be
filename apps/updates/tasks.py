import logging

from celery import shared_task
from updates.bulovka.loaders import ExternalReferenceError
from updates.models import Source

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
    source = Source.objects.get_or_create_from_settings(name=source_name)
    source.update(full_update=full_update, **kwargs)
