import datetime

import factory
from django.conf import settings
from factory import fuzzy
from updates.models import Source, Update


class SourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Source
        django_get_or_create = ["name"]

    name = factory.Iterator(settings.UPDATE_SOURCES.keys())


class UpdateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Update

    source = factory.SubFactory(SourceFactory)
    started_at = fuzzy.FuzzyDateTime(
        datetime.datetime(2021, 10, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2021, 11, 1, tzinfo=datetime.timezone.utc),
    )
    finished_at = None
