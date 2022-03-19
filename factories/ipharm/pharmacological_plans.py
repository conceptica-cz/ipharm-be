import random

import factory
from django.utils import timezone

from factories.ipharm import CareFactory
from factories.references import TagFactory


class PharmacologicalPlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "ipharm.PharmacologicalPlan"

    care = factory.SubFactory(CareFactory)
    text = factory.Faker("text", locale="la")
    his_text = factory.Faker("text", locale="la")
    note = factory.Faker("text", locale="la")
    notification_datetime = factory.Faker(
        "date_time_this_year", before_now=True, after_now=False, tzinfo=timezone.utc
    )

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if create:
            for _ in range(random.randint(1, 4)):
                self.tags.add(TagFactory())


class PharmacologicalPlanCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "ipharm.PharmacologicalPlanComment"

    pharmacological_plan = factory.SubFactory(PharmacologicalPlanFactory)
    comment_type = factory.Iterator(["comment", "verification"])
    text = factory.Faker("text", locale="la")
