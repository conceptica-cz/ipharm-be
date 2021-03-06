# Generated by Django 3.2.12 on 2022-03-10 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipharm', '0023_pharmacological_evaluation_care_related_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpharmacologicalevaluation',
            name='dose_change_hepatic_insufficiency',
            field=models.BooleanField(default=False, help_text='Hepatální insuficience'),
        ),
        migrations.AlterField(
            model_name='historicalpharmacologicalevaluation',
            name='dose_change_renal_insufficiency',
            field=models.BooleanField(default=False, help_text='Renální insuficience'),
        ),
        migrations.AlterField(
            model_name='pharmacologicalevaluation',
            name='dose_change_hepatic_insufficiency',
            field=models.BooleanField(default=False, help_text='Hepatální insuficience'),
        ),
        migrations.AlterField(
            model_name='pharmacologicalevaluation',
            name='dose_change_renal_insufficiency',
            field=models.BooleanField(default=False, help_text='Renální insuficience'),
        ),
    ]
