# Generated by Django 3.2.12 on 2022-03-16 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0021_identification_pcz'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='provider_code',
            field=models.CharField(blank=True, help_text='Kód poskytovatele', max_length=3),
        ),
        migrations.AddField(
            model_name='department',
            name='workplace_code',
            field=models.CharField(blank=True, help_text='Zkrácený kód pracoviště dle ÚZIS', max_length=10),
        ),
        migrations.AddField(
            model_name='historicaldepartment',
            name='provider_code',
            field=models.CharField(blank=True, help_text='Kód poskytovatele', max_length=3),
        ),
        migrations.AddField(
            model_name='historicaldepartment',
            name='workplace_code',
            field=models.CharField(blank=True, help_text='Zkrácený kód pracoviště dle ÚZIS', max_length=10),
        ),
    ]
