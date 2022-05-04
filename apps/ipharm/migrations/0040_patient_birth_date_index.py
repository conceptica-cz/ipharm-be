# Generated by Django 3.2.13 on 2022-05-04 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipharm', '0039_checkin_toggle_diagnoses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpatient',
            name='birth_date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='birth_date',
            field=models.DateField(db_index=True),
        ),
    ]
