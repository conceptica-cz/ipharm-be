# Generated by Django 3.2.13 on 2022-06-14 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipharm', '0044_care_patient_related_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalriskdrughistorydiagnosisdrug',
            old_name='check_in_diagnosis',
            new_name='risk_drug_history_diagnosis',
        ),
        migrations.RenameField(
            model_name='riskdrughistorydiagnosisdrug',
            old_name='check_in_diagnosis',
            new_name='risk_drug_history_diagnosis',
        ),
    ]
