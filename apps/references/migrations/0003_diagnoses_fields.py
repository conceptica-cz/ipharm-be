# Generated by Django 3.2.9 on 2021-12-09 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnosis',
            name='acceptable_gender',
            field=models.CharField(blank=True, help_text='Přípustné pohlaví', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='age_from',
            field=models.CharField(blank=True, help_text='Věk od', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='age_to',
            field=models.CharField(blank=True, help_text='Věk do', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='death_cause',
            field=models.CharField(blank=True, help_text='Skupina diagnóz příčin smrti', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='diagnosis_class',
            field=models.CharField(blank=True, help_text='Třída diagnózy', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='inadmissible_gender',
            field=models.CharField(blank=True, help_text='Nepřípustné pohlaví', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='m5dg',
            field=models.CharField(blank=True, help_text='Členění na pátém místě', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='mkn_conversion',
            field=models.CharField(blank=True, help_text='Převod na dg MKN-9', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='ncd_diagnosis_group',
            field=models.CharField(blank=True, help_text='Skupina diagnóz pro NZIS', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='primary_diagnosis_dg',
            field=models.CharField(blank=True, help_text='Základní diagnóza v případě *Dg', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='skupla_1',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='skupla_2',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='skupla_3',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='skupla_4',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='skupla_5',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='skupla_6',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='skupla_7',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='skupla_8',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='skupla_9',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='type_character',
            field=models.CharField(blank=True, help_text='Znak pro označení druhu diagnózy (+*-)', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='valid_from',
            field=models.DateField(blank=True, help_text='Platnost od', null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='valid_to',
            field=models.DateField(blank=True, help_text='Platnost do', null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='who_group_1',
            field=models.CharField(blank=True, help_text='Skupina diagnóz č. 1 WHO', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='who_group_2',
            field=models.CharField(blank=True, help_text='Skupina diagnóz č. 2 WHO', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='who_group_3',
            field=models.CharField(blank=True, help_text='Skupina diagnóz č. 3 WHO', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='who_group_4',
            field=models.CharField(blank=True, help_text='Skupina diagnóz č. 4 WHO', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='who_group_5',
            field=models.CharField(blank=True, help_text='Skupina diagnóz č. 5 WHO', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='acceptable_gender',
            field=models.CharField(blank=True, help_text='Přípustné pohlaví', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='age_from',
            field=models.CharField(blank=True, help_text='Věk od', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='age_to',
            field=models.CharField(blank=True, help_text='Věk do', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='death_cause',
            field=models.CharField(blank=True, help_text='Skupina diagnóz příčin smrti', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='diagnosis_class',
            field=models.CharField(blank=True, help_text='Třída diagnózy', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='inadmissible_gender',
            field=models.CharField(blank=True, help_text='Nepřípustné pohlaví', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='m5dg',
            field=models.CharField(blank=True, help_text='Členění na pátém místě', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='mkn_conversion',
            field=models.CharField(blank=True, help_text='Převod na dg MKN-9', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='ncd_diagnosis_group',
            field=models.CharField(blank=True, help_text='Skupina diagnóz pro NZIS', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='primary_diagnosis_dg',
            field=models.CharField(blank=True, help_text='Základní diagnóza v případě *Dg', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='skupla_1',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='skupla_2',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='skupla_3',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='skupla_4',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='skupla_5',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='skupla_6',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='skupla_7',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='skupla_8',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='skupla_9',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='type_character',
            field=models.CharField(blank=True, help_text='Znak pro označení druhu diagnózy (+*-)', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='valid_from',
            field=models.DateField(blank=True, help_text='Platnost od', null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='valid_to',
            field=models.DateField(blank=True, help_text='Platnost do', null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='who_group_1',
            field=models.CharField(blank=True, help_text='Skupina diagnóz č. 1 WHO', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='who_group_2',
            field=models.CharField(blank=True, help_text='Skupina diagnóz č. 2 WHO', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='who_group_3',
            field=models.CharField(blank=True, help_text='Skupina diagnóz č. 3 WHO', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='who_group_4',
            field=models.CharField(blank=True, help_text='Skupina diagnóz č. 4 WHO', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='who_group_5',
            field=models.CharField(blank=True, help_text='Skupina diagnóz č. 5 WHO', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='code',
            field=models.CharField(help_text='Kód', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='name',
            field=models.CharField(blank=True, help_text='Název', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='historicaldiagnosis',
            name='code',
            field=models.CharField(db_index=True, help_text='Kód', max_length=10),
        ),
        migrations.AlterField(
            model_name='historicaldiagnosis',
            name='name',
            field=models.CharField(blank=True, help_text='Název', max_length=100, null=True),
        ),
    ]
