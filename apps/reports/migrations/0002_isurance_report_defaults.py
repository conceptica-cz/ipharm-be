# Generated by Django 3.2.11 on 2022-01-27 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalinsurancereport',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='historicalinsurancereport',
            name='data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='insurancereport',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='insurancereport',
            name='data',
            field=models.JSONField(default=dict),
        ),
    ]
