# Generated by Django 3.2.11 on 2022-01-21 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0006_clinic_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalinsurancecompany',
            name='city',
            field=models.CharField(blank=True, help_text='Město', max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalinsurancecompany',
            name='zip',
            field=models.CharField(blank=True, help_text='PSČ', max_length=20),
        ),
        migrations.AlterField(
            model_name='insurancecompany',
            name='city',
            field=models.CharField(blank=True, help_text='Město', max_length=50),
        ),
        migrations.AlterField(
            model_name='insurancecompany',
            name='zip',
            field=models.CharField(blank=True, help_text='PSČ', max_length=20),
        ),
    ]
