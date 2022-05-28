from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone


class UpdateQuerySet(QuerySet):
    def get_old_empty_updates(self):
        threshold = timezone.now() - timezone.timedelta(
            hours=settings.EMPTY_UPDATES_DELETING_TIME_GAP
        )
        queryset = self.filter(modelupdate__isnull=True, started_at__lt=threshold)
        return queryset


class ModelUpdateQuerySet(QuerySet):
    def get_old_empty_updates(self):
        threshold = timezone.now() - timezone.timedelta(
            hours=settings.EMPTY_UPDATES_DELETING_TIME_GAP
        )
        queryset = self.filter(created=0, updated=0, created_at__lt=threshold)
        return queryset
