# Generated by Django 3.2.12 on 2022-02-26 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0020_clinic_reference_id'),
        ('ipharm', '0016_checkin_medical_rpocedure'),
    ]

    operations = [
        migrations.AddField(
            model_name='care',
            name='external_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='references.externaldepartment'),
        ),
        migrations.AddField(
            model_name='historicalcare',
            name='external_department',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='references.externaldepartment'),
        ),
        migrations.AlterField(
            model_name='care',
            name='care_type',
            field=models.CharField(choices=[('hospitalization', 'Hospitalization'), ('ambulation', 'Ambulation'), ('external', 'External')], default='ambulation', max_length=20),
        ),
        migrations.AlterField(
            model_name='care',
            name='clinic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='references.clinic'),
        ),
        migrations.AlterField(
            model_name='historicalcare',
            name='care_type',
            field=models.CharField(choices=[('hospitalization', 'Hospitalization'), ('ambulation', 'Ambulation'), ('external', 'External')], default='ambulation', max_length=20),
        ),
    ]