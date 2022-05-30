import factory
from requisitions.models.requisitions import Requisition


class RequisitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Requisition

    external_id = factory.Sequence(lambda n: n)
    type = Requisition.TYPE_IPHARM
    subtype = Requisition.SUBTYPE_IPHARM_CONCILATION
    state = Requisition.STATE_CREATED
    patient = factory.SubFactory("factories.ipharm.patients.PatientFactory")
    text = factory.Faker("text")
    file = None
    applicant = factory.SubFactory("factories.references.persons.PersonFactory")
    solver = factory.SubFactory("factories.references.persons.PersonFactory")
    is_synced = False
