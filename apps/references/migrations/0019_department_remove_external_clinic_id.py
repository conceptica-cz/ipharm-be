# Generated by Django 3.2.11 on 2022-02-09 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0018_external_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='clinic_external_id',
        ),
        migrations.RemoveField(
            model_name='historicaldepartment',
            name='clinic_external_id',
        ),
    ]
