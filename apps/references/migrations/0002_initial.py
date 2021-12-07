# Generated by Django 3.2.9 on 2021-12-07 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('updates', '0001_initial'),
        ('references', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltag',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaltag',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.update'),
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='history_relation',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history', to='references.person'),
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.update'),
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
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.update'),
        ),
        migrations.AddField(
            model_name='historicalidentification',
            name='history_relation',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history', to='references.identification'),
        ),
        migrations.AddField(
            model_name='historicalidentification',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalidentification',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.update'),
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
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.update'),
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
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.update'),
        ),
        migrations.AddField(
            model_name='historicaldepartment',
            name='clinic',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Klinika', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='references.clinic'),
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
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.update'),
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
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.update'),
        ),
        migrations.AddField(
            model_name='historicaladverseeffect',
            name='history_relation',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history', to='references.adverseeffect'),
        ),
        migrations.AddField(
            model_name='historicaladverseeffect',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaladverseeffect',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.update'),
        ),
        migrations.AddField(
            model_name='department',
            name='clinic',
            field=models.ForeignKey(help_text='Klinika', on_delete=django.db.models.deletion.CASCADE, to='references.clinic'),
        ),
        migrations.AddIndex(
            model_name='clinic',
            index=models.Index(fields=['description'], name='references__descrip_4ee902_idx'),
        ),
        migrations.AddIndex(
            model_name='adverseeffect',
            index=models.Index(fields=['name'], name='references__name_9815dd_idx'),
        ),
        migrations.AddIndex(
            model_name='department',
            index=models.Index(fields=['description'], name='references__descrip_30cdc7_idx'),
        ),
    ]
