import django_filters
from ipharm.models.patient_informations import PatientInformation


class PatientInformationFilter(django_filters.FilterSet):
    patient = django_filters.NumberFilter(field_name="care__patient__pk")
    care = django_filters.NumberFilter(field_name="care__pk")
