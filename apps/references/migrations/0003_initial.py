# Generated by Django 3.2.9 on 2021-11-21 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('references', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('updates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalperson',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='update',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='updates.referenceupdate'),
        ),
        migrations.AddField(
            model_name='historicalinsurancecompany',
            name='history_relation',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history', to='references.insurancecompany'),
        ),
        migrations.AddField(
            model_name='historicalinsurancecompany',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalinsurancecompany',
            name='update',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='updates.referenceupdate'),
        ),
        migrations.AddField(
            model_name='historicaldrug',
            name='history_relation',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history', to='references.drug'),
        ),
        migrations.AddField(
            model_name='historicaldrug',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaldrug',
            name='update',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='updates.referenceupdate'),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='history_relation',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history', to='references.diagnosis'),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaldiagnosis',
            name='update',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='updates.referenceupdate'),
        ),
        migrations.AddField(
            model_name='historicaldepartment',
            name='clinic',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='references.clinic'),
        ),
        migrations.AddField(
            model_name='historicaldepartment',
            name='history_relation',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history', to='references.department'),
        ),
        migrations.AddField(
            model_name='historicaldepartment',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaldepartment',
            name='update',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='updates.referenceupdate'),
        ),
        migrations.AddField(
            model_name='historicalclinic',
            name='history_relation',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history', to='references.clinic'),
        ),
        migrations.AddField(
            model_name='historicalclinic',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalclinic',
            name='update',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='updates.referenceupdate'),
        ),
        migrations.AddField(
            model_name='drug',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.referenceupdate'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.referenceupdate'),
        ),
        migrations.AddField(
            model_name='department',
            name='clinic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='references.clinic'),
        ),
        migrations.AddField(
            model_name='department',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.referenceupdate'),
        ),
        migrations.AddField(
            model_name='clinic',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.referenceupdate'),
        ),
    ]
