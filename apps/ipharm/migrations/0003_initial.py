# Generated by Django 3.2.8 on 2021-10-31 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('updates', '0001_initial'),
        ('references', '0001_initial'),
        ('ipharm', '0002_patient_clinic'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.referenceupdate'),
        ),
        migrations.AddField(
            model_name='historicalpatient',
            name='clinic',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='references.clinic'),
        ),
    ]
