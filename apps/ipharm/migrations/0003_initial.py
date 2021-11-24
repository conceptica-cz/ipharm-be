# Generated by Django 3.2.9 on 2021-11-24 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('updates', '0001_initial'),
        ('ipharm', '0002_patient_insurance_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.referenceupdate'),
        ),
        migrations.AddField(
            model_name='historicalpatient',
            name='current_ambulance_care',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ipharm.care'),
        ),
        migrations.AddField(
            model_name='historicalpatient',
            name='current_hospital_care',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ipharm.care'),
        ),
        migrations.AddField(
            model_name='historicalpatient',
            name='history_relation',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history', to='ipharm.patient'),
        ),
    ]
