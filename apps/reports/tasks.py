import logging

from celery import shared_task
from django.utils import timezone
from reports.insurance_report import generate_all_reports

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    ignore_result=True,
)
def generate_insurance_report(self):
    logger.info("Task generate has been started. task_id: %s", self.request.id)
    now = timezone.now()
    generate_all_reports(year=now.year, month=now.month)
    logger.info("Task generate has been finished. task_id: %s", self.request.id)
