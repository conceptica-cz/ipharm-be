# Generated by Django 3.2.11 on 2022-02-02 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipharm', '0009_createdat_default'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkin',
            name='for_insurance',
        ),
        migrations.RemoveField(
            model_name='historicalcheckin',
            name='for_insurance',
        ),
        migrations.AddField(
            model_name='checkin',
            name='in_insurance_report',
            field=models.BooleanField(default=False, help_text='Je ve vykazování'),
        ),
        migrations.AddField(
            model_name='historicalcheckin',
            name='in_insurance_report',
            field=models.BooleanField(default=False, help_text='Je ve vykazování'),
        ),
    ]
