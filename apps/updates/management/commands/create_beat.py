import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Create django celery beat periodic tasks"

    def handle(self, *args, **options):
        print("Creating django celery beat periodic tasks...")
        for name in settings.UPDATE_SOURCES:
            interval_schedule, _ = IntervalSchedule.objects.get_or_create(
                every=settings.UPDATE_SOURCES[name].get(
                    "interval", settings.DEFAULT_INCREMENTAL_UPDATE_INTERVAL
                ),
                period=IntervalSchedule.MINUTES,
            )
            task_name = f"{name} incremental"
            PeriodicTask.objects.update_or_create(
                name=task_name,
                defaults={
                    "task": "updates.tasks.update",
                    "interval": interval_schedule,
                    "kwargs": json.dumps({"source_name": name}),
                },
            )
            task_name = f"{name} full"
            full_schedule, _ = IntervalSchedule.objects.get_or_create(
                every=settings.UPDATE_SOURCES[name].get(
                    "interval", settings.DEFAULT_FULL_UPDATE_INTERVAL
                ),
                period=IntervalSchedule.MINUTES,
            )
            PeriodicTask.objects.update_or_create(
                name=task_name,
                defaults={
                    "task": "updates.tasks.update",
                    "interval": full_schedule,
                    "kwargs": json.dumps({"source_name": name, "full_update": True}),
                },
            )
        print("Done.")
