# Generated by Django 3.2.13 on 2022-06-10 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipharm', '0042_risk_drug_history_diagnoses_drugs'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='checkindiagnosis',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='riskdrughistorydiagnosis',
            unique_together=set(),
        ),
    ]
