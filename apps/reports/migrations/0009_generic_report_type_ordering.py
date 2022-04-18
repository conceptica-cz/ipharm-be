# Generated by Django 3.2.12 on 2022-04-18 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0008_generic_report_file_time_range'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genericreporttype',
            options={'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='genericreporttype',
            name='order',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
