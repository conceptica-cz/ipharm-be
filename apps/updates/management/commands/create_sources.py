from django.conf import settings
from django.core.management.base import BaseCommand
from updates.models import Source


class Command(BaseCommand):
    help = "Create update Source models from settings"

    def handle(self, *args, **options):
        for name in settings.UPDATE_SOURCES:
            Source.objects.get_or_create_from_settings(name=name)
