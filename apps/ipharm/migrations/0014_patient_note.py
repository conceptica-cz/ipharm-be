# Generated by Django 3.2.11 on 2022-02-04 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipharm', '0013_patient_delete_legacy_current_care'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpatient',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='note',
            field=models.TextField(blank=True),
        ),
    ]
