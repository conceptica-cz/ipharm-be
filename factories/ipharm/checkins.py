import random

import factory
from ipharm.models import CheckIn

from factories.ipharm.cares import CareFactory
from factories.references.drugs import DrugFactory


class CheckInFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CheckIn

    class Params:
        polypharmacy_decider = factory.Iterator([True, False])

    care = factory.SubFactory(CareFactory)

    @factory.post_generation
    def drugs(self, create, extracted, **kwargs):
        if not create:
            return
        elif extracted:
            for drug in extracted:
                self.drugs.add(drug)
        else:
            print("Creating drugs")
            for _ in range(random.randint(1, 3)):
                self.drugs.add(DrugFactory())
