from django.db import models
from updates.models import BaseUpdatableModel


class MedicalFacility(BaseUpdatableModel):
    facility_id = models.CharField(
        max_length=50, unique=True, help_text="ID zdravotnického zařízení"
    )
    code = models.CharField(
        max_length=50, unique=True, help_text="Kód zdravotnického zařízení"
    )
    name = models.CharField(max_length=255, help_text="Název zdravotnického zařízení")
    provision_place_id = models.CharField(
        max_length=50, null=True, blank=True, help_text="ID Místa poskytování"
    )
    facility_type = models.CharField(
        max_length=255, null=True, blank=True, help_text="Druh zařízení"
    )
    city = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Adresa místa poskytování: Obec",
    )
    postal_code = models.CharField(
        max_length=100, null=True, blank=True, help_text="Adresa místa poskytování: PSČ"
    )
    street = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Adresa místa poskytování: Ulice",
    )
    street_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Adresa místa poskytování: Č. orientační",
    )
    region = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Adresa místa poskytování: Kraj",
    )
    region_code = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Adresa místa poskytování: Kraj",
    )
    district = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Adresa místa poskytování: Okres",
    )
    district_code = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Adresa místa poskytování: Kód okresu",
    )
    administrative_district = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Adresa místa poskytování: Správní obvod (např. Praha)",
    )
    phone = models.CharField(
        max_length=100, null=True, blank=True, help_text="Poskytovatel: Telefon"
    )
    fax = models.CharField(
        max_length=100, null=True, blank=True, help_text="Poskytovatel: Fax"
    )
    email = models.CharField(
        max_length=255, null=True, blank=True, help_text="Poskytovatel: Email"
    )
    web = models.CharField(
        max_length=255, null=True, blank=True, help_text="Poskytovatel: Web"
    )
    ico = models.CharField(
        max_length=100, null=True, blank=True, help_text="IČO poskytovatele"
    )
    founder_legal_form = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Zřizovatel: Typ právnické osoby",
    )
    founder_legal_form_code = models.CharField(
        max_length=100, null=True, blank=True, help_text="Zřizovatel: Kód právní formy"
    )
    founder_city = models.CharField(
        max_length=100, null=True, blank=True, help_text="Zřizovatel adresa sídla: Obec"
    )
    founder_postal_code = models.CharField(
        max_length=100, null=True, blank=True, help_text="Zřizovatel adresa sídla: PSČ"
    )
    founder_street = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Zřizovatel adresa sídla: Ulice",
    )
    founder_street_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Zřizovatel adresa sídla: Č. orientační",
    )
    founder_region_code = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Zřizovatel adresa sídla: Kód kraje",
    )
    founder_district_code = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Zřizovatel adresa sídla: Kód okresu",
    )
    care_field_values = models.TextField(
        null=True, blank=True, help_text="Textové hodnoty z číselníku OborPece"
    )
    care_form_values = models.TextField(
        null=True, blank=True, help_text="Textové hodnoty z číselníku FormaPece"
    )
    care_type_values = models.TextField(
        null=True, blank=True, help_text="Textové hodnoty z číselníku DruhPece"
    )
    representative = models.TextField(
        null=True, blank=True, help_text="Odborný zástupce"
    )
    longitude = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="GPS souřadnice místa poskytování, WGS84 šířka",
    )
    latitude = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="GPS souřadnice místa poskytování, WGS84 délka",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Medical Facility"
        verbose_name_plural = "Medical Facilities"
