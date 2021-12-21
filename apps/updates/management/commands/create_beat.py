import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask
from references.models import Clinic

EXTERNAL_SOURCES = ["Patient"]


class Command(BaseCommand):
    help = "Create django celery beat periodic tasks"

    def handle(self, *args, **options):
        print("Creating django celery beat periodic tasks...")
        for name in settings.UPDATE_SOURCES:
            if name in EXTERNAL_SOURCES:
                self._create_external_beat(name)
            else:
                self._create_reference_beat(name)
        print("Done.")

    @staticmethod
    def _create_reference_beat(name):
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

    @staticmethod
    def _create_external_beat(name):
        december_first, _ = CrontabSchedule.objects.get_or_create(
            minute="0", hour="0", day_of_week="*", day_of_month="1", month_of_year="12"
        )
        if settings.UPDATE_SOURCES[name].get("by_clinic", False):
            for clinic in Clinic.objects.filter(is_ambulance=True):
                task_name = f"{name} /Clinic {clinic.id}"
                PeriodicTask.objects.update_or_create(
                    name=task_name,
                    defaults={
                        "task": "updates.tasks.update",
                        "crontab": december_first,
                        "kwargs": json.dumps(
                            {
                                "source_name": name,
                                "full_update": True,
                                "clinic_id": clinic.id,
                            }
                        ),
                    },
                )
        else:
            task_name = f"{name}"
            PeriodicTask.objects.update_or_create(
                name=task_name,
                defaults={
                    "task": "updates.tasks.update",
                    "crontab": december_first,
                    "kwargs": json.dumps(
                        {
                            "source_name": name,
                            "full_update": True,
                        }
                    ),
                },
            )
