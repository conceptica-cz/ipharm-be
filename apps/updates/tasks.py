from celery import shared_task
from updates.models import Source
from updates.updater import Updater


@shared_task()
def update(source_name: str, full_update=False):
    source = Source.objects.get_or_create_from_settings(name=source_name)
    source.update(full_update=full_update)
