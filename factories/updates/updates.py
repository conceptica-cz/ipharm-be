import datetime

import factory
from django.conf import settings
from factory import fuzzy
from updates.models import Reference, ReferenceUpdate


class ReferenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reference
        django_get_or_create = ["model"]

    model = factory.Iterator(settings.REFERENCES.keys())
    name = factory.Iterator(settings.REFERENCES.values(), getter=lambda r: r["name"])


class ReferenceUpdateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReferenceUpdate

    reference = factory.SubFactory(ReferenceFactory)
    started_at = fuzzy.FuzzyDateTime(
        datetime.datetime(2021, 10, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2021, 11, 1, tzinfo=datetime.timezone.utc),
    )
    finished_at = None
