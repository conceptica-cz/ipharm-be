# Generated by Django 3.2.12 on 2022-04-06 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipharm', '0035_pharmacologicalplan_add_m2m'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='riskdrughistory',
            name='risk_diagnoses',
        ),
        migrations.RemoveField(
            model_name='riskdrughistory',
            name='risk_drugs',
        ),
        migrations.RemoveField(
            model_name='riskdrughistory',
            name='tags',
        ),
    ]
