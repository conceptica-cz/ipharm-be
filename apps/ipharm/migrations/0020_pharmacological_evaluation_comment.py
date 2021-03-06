# Generated by Django 3.2.12 on 2022-03-04 10:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0003_udpate_url_parameters'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ipharm', '0019_risk_drug_history_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='PharmacologicalEvaluationComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('text', models.TextField(blank=True, help_text='Komentář', null=True)),
                ('pharmacological_evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipharm.pharmacologicalevaluation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalPharmacologicalEvaluationComment',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('text', models.TextField(blank=True, help_text='Komentář', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_relation', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history', to='ipharm.pharmacologicalevaluationcomment')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('pharmacological_evaluation', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ipharm.pharmacologicalevaluation')),
                ('update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.update')),
            ],
            options={
                'verbose_name': 'historical pharmacological evaluation comment',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
