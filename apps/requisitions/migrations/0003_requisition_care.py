# Generated by Django 3.2.13 on 2022-05-31 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ipharm', '0040_patient_birth_date_index'),
        ('requisitions', '0002_requisition_updated_at_auto_now'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalrequisition',
            name='care',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ipharm.care'),
        ),
        migrations.AddField(
            model_name='requisition',
            name='care',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requisitions', to='ipharm.care'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requisitions', to='ipharm.patient'),
        ),
    ]
