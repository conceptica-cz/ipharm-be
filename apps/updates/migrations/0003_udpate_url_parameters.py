# Generated by Django 3.2.10 on 2022-01-10 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalupdate',
            name='url_parameters',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='update',
            name='url_parameters',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
