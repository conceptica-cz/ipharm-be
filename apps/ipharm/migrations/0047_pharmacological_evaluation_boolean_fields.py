# Generated by Django 3.2.14 on 2022-07-14 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipharm', '0046_comments_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpharmacologicalevaluation',
            name='administration_method_optimization',
            field=models.BooleanField(default=False, help_text='Optimalizace způsobu poddání'),
        ),
        migrations.AlterField(
            model_name='historicalpharmacologicalevaluation',
            name='dosage_determination',
            field=models.BooleanField(default=False, help_text='Stanovení dávky (při zahájení terapie)'),
        ),
        migrations.AlterField(
            model_name='pharmacologicalevaluation',
            name='administration_method_optimization',
            field=models.BooleanField(default=False, help_text='Optimalizace způsobu poddání'),
        ),
        migrations.AlterField(
            model_name='pharmacologicalevaluation',
            name='dosage_determination',
            field=models.BooleanField(default=False, help_text='Stanovení dávky (při zahájení terapie)'),
        ),
    ]