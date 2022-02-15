# Generated by Django 3.2.11 on 2022-02-03 14:07

from django.db import migrations


def move_current_care(apps, schema_editor):
    Patient = apps.get_model("ipharm", "Patient")
    for patient in Patient.objects.all():
        print(f"Migarting patient {patient.id}")
        if patient.current_hospital_care:
            patient.current_care = patient.current_hospital_care
            patient.save()
        elif patient.current_ambulance_care:
            patient.current_care = patient.current_ambulance_care
            patient.save()


def reverse(apps, schema_editor):
    Patient = apps.get_model("ipharm", "Patient")
    for patient in Patient.objects.all():
        print(f"Reverse migarting patient {patient.id}")
        if patient.current_care:
            if patient.current_care.care_type == "hospitalization":
                patient.current_hospital_care = patient.current_care
                patient.save()
            elif patient.current_care.care_type == "ambulation":
                patient.current_ambulance_care = patient.current_care
                patient.save()


class Migration(migrations.Migration):

    dependencies = [
        ("ipharm", "0011_patient_add_current_care"),
    ]

    operations = [migrations.RunPython(move_current_care, reverse)]