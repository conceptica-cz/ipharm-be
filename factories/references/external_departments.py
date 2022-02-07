import factory
from references.models import ExternalDepartment


class ExternalDepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExternalDepartment
        django_get_or_create = ["icp"]

    icp = factory.Sequence(lambda n: n)
    organization = factory.LazyAttribute(lambda o: f"Organization {o.icp}")
    department = factory.LazyAttribute(lambda o: f"Department {o.icp}")
    specialization_code = factory.Iterator(range(1, 1000))
