# Generated by Django 3.2.11 on 2022-02-15 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0019_department_remove_external_clinic_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='reference_id',
            field=models.IntegerField(blank=True, help_text='iČíselník Kód', null=True, unique=True),
        ),
        migrations.AddField(
            model_name='historicalclinic',
            name='reference_id',
            field=models.IntegerField(blank=True, db_index=True, help_text='iČíselník Kód', null=True),
        ),
    ]
