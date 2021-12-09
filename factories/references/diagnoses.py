import factory
from references.models.diagnoses import Diagnosis

CODES = [
    "A00",
    "A000",
    "A001",
    "A009",
    "A01",
    "A010",
    "A011",
    "A012",
    "A013",
    "A014",
    "A02",
    "A020",
    "A021",
    "A022",
    "A028",
    "A029",
    "A03",
    "A030",
    "A031",
    "A032",
    "A033",
    "A038",
    "A039",
    "A04",
    "A040",
    "A041",
]


class DiagnosisFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Diagnosis
        django_get_or_create = ("code",)

    code = factory.Iterator(CODES)
    name = factory.Faker("sentence", nb_words=2, locale="la")
    m5dg = None
    type_character = None
    primary_diagnosis_dg = None
    death_cause = None
    inadmissible_gender = None
    acceptable_gender = None
    age_from = None
    age_to = None
    diagnosis_class = None
    who_group_1 = None
    who_group_2 = None
    who_group_3 = None
    who_group_4 = None
    who_group_5 = None
    ncd_diagnosis_group = None
    skupla_1 = None
    skupla_2 = None
    skupla_3 = None
    skupla_4 = None
    skupla_5 = None
    skupla_6 = None
    skupla_7 = None
    skupla_8 = None
    skupla_9 = None
    mkn_conversion = None
    valid_from = None
    valid_to = None
