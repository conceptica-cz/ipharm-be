# Generated by Django 3.2.12 on 2022-04-06 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipharm', '0029_alter_patientinformation_care'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkin',
            name='diagnoses',
        ),
        migrations.RemoveField(
            model_name='checkin',
            name='diagnoses_drugs',
        ),
        migrations.RemoveField(
            model_name='checkin',
            name='drugs',
        ),
        migrations.RemoveField(
            model_name='checkin',
            name='high_interaction_potential_drugs',
        ),
        migrations.RemoveField(
            model_name='checkin',
            name='narrow_therapeutic_window_drugs',
        ),
    ]
