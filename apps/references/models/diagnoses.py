from django.db import models
from references.managers.diagnosis import DiagnosisManager
from updates.models import BaseUpdatableModel


class Diagnosis(BaseUpdatableModel):
    code = models.CharField(max_length=10, unique=True, help_text="Kód")
    name = models.CharField(max_length=100, null=True, blank=True, help_text="Název")
    m5dg = models.CharField(
        max_length=10, null=True, blank=True, help_text="Členění na pátém místě"
    )
    type_character = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Znak pro označení druhu diagnózy (+*-)",
    )
    primary_diagnosis_dg = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Základní diagnóza v případě *Dg",
    )
    death_cause = models.CharField(
        max_length=10, null=True, blank=True, help_text="Skupina diagnóz příčin smrti"
    )
    inadmissible_gender = models.CharField(
        max_length=10, null=True, blank=True, help_text="Nepřípustné pohlaví"
    )
    acceptable_gender = models.CharField(
        max_length=10, null=True, blank=True, help_text="Přípustné pohlaví"
    )
    age_from = models.CharField(
        max_length=10, null=True, blank=True, help_text="Věk od"
    )
    age_to = models.CharField(max_length=10, null=True, blank=True, help_text="Věk do")
    diagnosis_class = models.CharField(
        max_length=10, null=True, blank=True, help_text="Třída diagnózy"
    )
    who_group_1 = models.CharField(
        max_length=10, null=True, blank=True, help_text="Skupina diagnóz č. 1 WHO"
    )
    who_group_2 = models.CharField(
        max_length=10, null=True, blank=True, help_text="Skupina diagnóz č. 2 WHO"
    )
    who_group_3 = models.CharField(
        max_length=10, null=True, blank=True, help_text="Skupina diagnóz č. 3 WHO"
    )
    who_group_4 = models.CharField(
        max_length=10, null=True, blank=True, help_text="Skupina diagnóz č. 4 WHO"
    )
    who_group_5 = models.CharField(
        max_length=10, null=True, blank=True, help_text="Skupina diagnóz č. 5 WHO"
    )
    ncd_diagnosis_group = models.CharField(
        max_length=10, null=True, blank=True, help_text="Skupina diagnóz pro NZIS"
    )
    skupla_1 = models.CharField(max_length=10, null=True, blank=True)
    skupla_2 = models.CharField(max_length=10, null=True, blank=True)
    skupla_3 = models.CharField(max_length=10, null=True, blank=True)
    skupla_4 = models.CharField(max_length=10, null=True, blank=True)
    skupla_5 = models.CharField(max_length=10, null=True, blank=True)
    skupla_6 = models.CharField(max_length=10, null=True, blank=True)
    skupla_7 = models.CharField(max_length=10, null=True, blank=True)
    skupla_8 = models.CharField(max_length=10, null=True, blank=True)
    skupla_9 = models.CharField(max_length=10, null=True, blank=True)
    mkn_conversion = models.CharField(
        max_length=10, null=True, blank=True, help_text="Převod na dg MKN-9"
    )
    valid_from = models.DateField(null=True, blank=True, help_text="Platnost od")
    valid_to = models.DateField(null=True, blank=True, help_text="Platnost do")

    objects = DiagnosisManager()

    class Meta:
        verbose_name = "Diagnosis"
        verbose_name_plural = "Diagnoses"

    def __str__(self):
        return self.name

    def serialize(self):
        from references.serializers import DiagnosisSerializer

        return DiagnosisSerializer(self)
