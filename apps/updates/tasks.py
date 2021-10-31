from celery import shared_task
from updates.updater import Updater


@shared_task()
def update(model: str):
    updater = Updater(model)
    updater.update()
