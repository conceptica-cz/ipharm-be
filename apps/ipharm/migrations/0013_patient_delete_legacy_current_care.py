# Generated by Django 3.2.11 on 2022-02-03 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipharm', '0012_patient_migrate_current_care'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalpatient',
            name='current_ambulance_care',
        ),
        migrations.RemoveField(
            model_name='historicalpatient',
            name='current_hospital_care',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='current_ambulance_care',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='current_hospital_care',
        ),
    ]