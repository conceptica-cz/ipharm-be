import factory
from factory import fuzzy
from faker import Faker
from ipharm.models import Patient

from factories.references.insurances import InsuranceCompanyFactory


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patient
        django_get_or_create = ["birth_number"]

    class Params:
        first_name_male = factory.Faker("first_name_male", locale="cs")
        last_name_male = factory.Faker("last_name_male", locale="cs")
        first_name_female = factory.Faker("first_name_female", locale="cs")
        last_name_female = factory.Faker("last_name_female", locale="cs")
        gender = factory.Iterator(["MALE", "FEMALE"])

    external_id = factory.Sequence(lambda n: n)

    @factory.lazy_attribute
    def first_name(self):
        if self.gender == "MALE":
            return self.first_name_male
        else:
            return self.first_name_female

    @factory.lazy_attribute
    def last_name(self):
        if self.gender == "MALE":
            return self.last_name_male
        else:
            return self.last_name_female

    birth_date = factory.Faker("date_of_birth", minimum_age=18, maximum_age=95)

    @factory.lazy_attribute
    def birth_number(self):
        birth = self.birth_date.strftime("%y%m%d")
        return f"{birth}{Faker().pyint(1000, 9999)}"

    insurance_company = factory.SubFactory(InsuranceCompanyFactory)
    insurance_number = fuzzy.FuzzyInteger(1000000000, 9999999999)
    height = fuzzy.FuzzyInteger(130, 210)
    weight = factory.LazyAttribute(lambda obj: obj.height - 100 + Faker().pyint(0, 40))
