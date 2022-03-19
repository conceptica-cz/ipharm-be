# Generated by Django 3.2.12 on 2022-03-18 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0023_department_remove_provider_code'),
        ('ipharm', '0025_pharmacological_evaluation_command_createdat'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpharmacologicalplan',
            name='medical_procedure',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='references.medicalprocedure'),
        ),
        migrations.AddField(
            model_name='historicalpharmacologicalplancomment',
            name='medical_procedure',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='references.medicalprocedure'),
        ),
        migrations.AddField(
            model_name='pharmacologicalplan',
            name='medical_procedure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='references.medicalprocedure'),
        ),
        migrations.AddField(
            model_name='pharmacologicalplancomment',
            name='medical_procedure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='references.medicalprocedure'),
        ),
    ]
