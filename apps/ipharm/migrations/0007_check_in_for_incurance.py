# Generated by Django 3.2.11 on 2022-01-27 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipharm', '0006_add_createat_updateat'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='for_insurance',
            field=models.BooleanField(default=False, help_text='Používat pro vykazování pojištění'),
        ),
        migrations.AddField(
            model_name='historicalcheckin',
            name='for_insurance',
            field=models.BooleanField(default=False, help_text='Používat pro vykazování pojištění'),
        ),
    ]