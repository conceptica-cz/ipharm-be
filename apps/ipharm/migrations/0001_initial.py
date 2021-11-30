# Generated by Django 3.2.9 on 2021-11-30 14:44

from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Care',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('care_type', models.CharField(choices=[('hospitalization', 'Hospitalization'), ('ambulation', 'Ambulation')], default='ambulation', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('external_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='UNIS ID')),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('polypharmacy', models.BooleanField(default=False, help_text='Polypragmazie')),
                ('polypharmacy_note', models.TextField(blank=True, help_text='Poznámka k polypragmazii', verbose_name='poznámka k polypragmazii')),
                ('high_interaction_potential', models.BooleanField(default=False, help_text='Léčiva s vysokým interakčním potenciálem', verbose_name='polypragmazie')),
                ('high_interaction_potential_note', models.TextField(blank=True, help_text='Poznámka k léčivám s vysokým interakčním potenciálem')),
                ('renal_insufficiency', models.BooleanField(default=False, help_text='Renální insuficience')),
                ('renal_insufficiency_note', models.TextField(blank=True, help_text='Poznámka k renální insuficience')),
                ('significant_biochemical_changes', models.BooleanField(default=False, help_text='Další významné změny biochemických nebo hematolologických parametrů')),
                ('significant_biochemical_changes_note', models.TextField(blank=True, help_text='Poznámka k dalším významným změnám biochemických nebo hematolologických parametrů')),
                ('systemic_corticosteroids', models.BooleanField(default=False, help_text='Systémové kortikoidy nebo jiné imunosupresiva')),
                ('systemic_corticosteroids_note', models.TextField(blank=True, help_text='Poznámka k systémovým kortikoidům nebo jiným imunosupresivům')),
                ('narrow_therapeutic_window', models.BooleanField(default=False, help_text='Léčiva s úzkým terapeutickým oknem')),
                ('narrow_therapeutic_window_note', models.TextField(blank=True, help_text='Poznámka k léčivům s úzkým terapeutickým oknem')),
                ('hepatic_insufficiency', models.BooleanField(default=False, help_text='Laboratorní známky hepatální insuficience')),
                ('hepatic_insufficiency_note', models.TextField(blank=True, help_text='Poznámka k laboratorním známkám hepatální insuficience')),
                ('intensive_care', models.BooleanField(default=False, help_text='Pacient v intenzivní péči')),
                ('intensive_care_note', models.TextField(blank=True, help_text='Poznámka k intenzivní péči')),
                ('pharmacist_intervention_required', models.BooleanField(default=False, help_text='Nutný zásah klinického farmaceuta')),
                ('consultation_requested', models.BooleanField(default=False, help_text='Vyžádané konzilium')),
                ('risk_level', models.CharField(choices=[('1', '1. stupeň'), ('2', '2. stupeň'), ('3', '3. stupeň')], default='1', help_text='Výsledný stupeň rizikovosti', max_length=1)),
                ('patient_condition_change', models.BooleanField(default=False, help_text='Změna stavu pacienta')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dekurz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('made_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalCare',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('care_type', models.CharField(choices=[('hospitalization', 'Hospitalization'), ('ambulation', 'Ambulation')], default='ambulation', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('external_id', models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='UNIS ID')),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical care',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCheckIn',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('polypharmacy', models.BooleanField(default=False, help_text='Polypragmazie')),
                ('polypharmacy_note', models.TextField(blank=True, help_text='Poznámka k polypragmazii', verbose_name='poznámka k polypragmazii')),
                ('high_interaction_potential', models.BooleanField(default=False, help_text='Léčiva s vysokým interakčním potenciálem', verbose_name='polypragmazie')),
                ('high_interaction_potential_note', models.TextField(blank=True, help_text='Poznámka k léčivám s vysokým interakčním potenciálem')),
                ('renal_insufficiency', models.BooleanField(default=False, help_text='Renální insuficience')),
                ('renal_insufficiency_note', models.TextField(blank=True, help_text='Poznámka k renální insuficience')),
                ('significant_biochemical_changes', models.BooleanField(default=False, help_text='Další významné změny biochemických nebo hematolologických parametrů')),
                ('significant_biochemical_changes_note', models.TextField(blank=True, help_text='Poznámka k dalším významným změnám biochemických nebo hematolologických parametrů')),
                ('systemic_corticosteroids', models.BooleanField(default=False, help_text='Systémové kortikoidy nebo jiné imunosupresiva')),
                ('systemic_corticosteroids_note', models.TextField(blank=True, help_text='Poznámka k systémovým kortikoidům nebo jiným imunosupresivům')),
                ('narrow_therapeutic_window', models.BooleanField(default=False, help_text='Léčiva s úzkým terapeutickým oknem')),
                ('narrow_therapeutic_window_note', models.TextField(blank=True, help_text='Poznámka k léčivům s úzkým terapeutickým oknem')),
                ('hepatic_insufficiency', models.BooleanField(default=False, help_text='Laboratorní známky hepatální insuficience')),
                ('hepatic_insufficiency_note', models.TextField(blank=True, help_text='Poznámka k laboratorním známkám hepatální insuficience')),
                ('intensive_care', models.BooleanField(default=False, help_text='Pacient v intenzivní péči')),
                ('intensive_care_note', models.TextField(blank=True, help_text='Poznámka k intenzivní péči')),
                ('pharmacist_intervention_required', models.BooleanField(default=False, help_text='Nutný zásah klinického farmaceuta')),
                ('consultation_requested', models.BooleanField(default=False, help_text='Vyžádané konzilium')),
                ('risk_level', models.CharField(choices=[('1', '1. stupeň'), ('2', '2. stupeň'), ('3', '3. stupeň')], default='1', help_text='Výsledný stupeň rizikovosti', max_length=1)),
                ('patient_condition_change', models.BooleanField(default=False, help_text='Změna stavu pacienta')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical check in',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalDekurz',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('made_at', models.DateTimeField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical dekurz',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPatient',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('external_id', models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='UNIS ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('birth_number', models.CharField(db_index=True, max_length=10)),
                ('insurance_number', models.CharField(blank=True, max_length=100, null=True)),
                ('height', models.FloatField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical patient',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPatientInformation',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text='Název záznamu', max_length=255)),
                ('text', models.TextField(blank=True, help_text='Popis', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical patient information',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPharmacologicalEvaluation',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deployment_initial_diagnosis', models.BooleanField(default=False, help_text='Diagnóza ve vstupní kontrole')),
                ('deployment_during_diagnosis', models.BooleanField(default=False, help_text='Diagnóza v průběhu hospitalizace')),
                ('deployment_ft_approach', models.BooleanField(default=False, help_text='Vhodnější FT přístup')),
                ('deployment_other_reason', models.TextField(blank=True, help_text='Jiný důvod', null=True)),
                ('discontinuation_contradiction', models.BooleanField(default=False, help_text='Kontraindikace')),
                ('discontinuation_adverse_effect', models.BooleanField(default=False, help_text='Projev nežádoucího účinku')),
                ('discontinuation_adverse_effect_risk', models.BooleanField(default=False, help_text='Riziko nežádoucího účinku')),
                ('discontinuation_missing_indication', models.BooleanField(default=False, help_text='Chybějící indikace')),
                ('discontinuation_allergies', models.BooleanField(default=False, help_text='Alergie')),
                ('discontinuation_drug_interaction', models.BooleanField(default=False, help_text='Léková interakce')),
                ('discontinuation_duplicity', models.BooleanField(default=False, help_text='Duplicity')),
                ('discontinuation_renal_insufficiency', models.BooleanField(default=False, help_text='Renální insuficience')),
                ('discontinuation_hepatic_insufficiency', models.BooleanField(default=False, help_text='Hepatální insuficience')),
                ('discontinuation_medical_intervention', models.BooleanField(default=False, help_text='Lékařská intervence')),
                ('discontinuation_underdosage', models.BooleanField(default=False, help_text='Poddávkování')),
                ('discontinuation_underdosage_risk', models.BooleanField(default=False, help_text='Rizika poddávkováí')),
                ('discontinuation_other_reason', models.TextField(blank=True, help_text='Jiný důvod', null=True)),
                ('dose_change_adverse_effect', models.BooleanField(default=False, help_text='Projev nežádoucího účinku')),
                ('dose_change_adverse_effect_risk', models.BooleanField(default=False, help_text='Riziko nežádoucího účinku')),
                ('dose_change_renal_insufficiency', models.BooleanField(default=False, help_text='Hepatální insuficience')),
                ('dose_change_hepatic_insufficiency', models.BooleanField(default=False, help_text='Renální insuficience')),
                ('dose_change_drug_interaction', models.BooleanField(default=False, help_text='Léková interakce')),
                ('dose_change_underdosage', models.BooleanField(default=False, help_text='Poddávkování')),
                ('dose_change_overdosage', models.BooleanField(default=False, help_text='Předávkování')),
                ('dose_change_laboratory_findings', models.BooleanField(default=False, help_text='Na základě laboratorních výseldků')),
                ('dose_change_dosage_reduction', models.BooleanField(default=False, help_text='Snížení dávky')),
                ('dose_change_dosage_increase', models.BooleanField(default=False, help_text='Zvýšení dávky')),
                ('dose_change_other_reason', models.TextField(blank=True, help_text='Jiný důvod', null=True)),
                ('continuation_drug_reintroduction', models.BooleanField(default=False, help_text='Znovunasazení léčiva')),
                ('continuation_medical_intervention', models.BooleanField(default=False, help_text='Po lékařské intervenci')),
                ('continuation_other_reason', models.TextField(blank=True, help_text='Jiný důvod', null=True)),
                ('tdm_interpretation', models.BooleanField(default=False, help_text='TDM - Interpretace')),
                ('tdm_measure_level_recommendation', models.BooleanField(default=False, help_text='TDM - Doporučení změření hladiny')),
                ('specific_adverse_effect_diagnosis', models.BooleanField(default=False, help_text='Specifika - Diagnostika nežádoucího účinku')),
                ('specific_adverse_effect_reporting', models.BooleanField(default=False, help_text='Specifika - Hlášení nežádoucího účinku')),
                ('specific_consultation', models.BooleanField(default=False, help_text='Specifika - Konzultace')),
                ('recommended_investigation_by_specialist', models.BooleanField(default=False, help_text='Doporučené vyšetření - Specialistou')),
                ('recommended_investigation_by_laboratory', models.BooleanField(default=False, help_text='Doporučené vyšetření - Laboratoří')),
                ('recommended_investigation_by_physical', models.BooleanField(default=False, help_text='Doporučené vyšetření - Fyzikální')),
                ('dosage_determination', models.TextField(blank=True, help_text='Stanovení dávky (při zahájení terapie)', null=True)),
                ('administration_method_optimization', models.TextField(blank=True, help_text='Optimalizace způsobu poddání', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical pharmacological evaluation',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPharmacologicalPlan',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('text', models.TextField(blank=True, help_text='Text farmakologického plánu', null=True)),
                ('his_text', models.TextField(blank=True, help_text='UNIS text', null=True)),
                ('note', models.TextField(blank=True, help_text='Poznámka', null=True)),
                ('notification_datetime', models.DateTimeField(blank=True, help_text='Datum pro upozornění', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical pharmacological plan',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPharmacologicalPlanComment',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('comment_type', models.CharField(choices=[('comment', 'Comment'), ('verification', 'Verification')], default='comment', max_length=20)),
                ('text', models.TextField(blank=True, help_text='Text', null=True)),
                ('verify', models.BooleanField(default=False, help_text='Vykázat ověření')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical pharmacological plan comment',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalRiskDrugHistory',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('has_risk_drug', models.BooleanField(default=False, help_text='Rizikové léčivo')),
                ('has_risk_diagnosis', models.BooleanField(default=False, help_text='Riziková diagnóza')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical risk drug history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalRiskDrugHistoryComment',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('text', models.TextField(help_text='Komentář')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical risk drug history comment',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('external_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='UNIS ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('birth_number', models.CharField(max_length=10, unique=True)),
                ('insurance_number', models.CharField(blank=True, max_length=100, null=True)),
                ('height', models.FloatField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='PatientInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text='Název záznamu', max_length=255)),
                ('text', models.TextField(blank=True, help_text='Popis', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PharmacologicalEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deployment_initial_diagnosis', models.BooleanField(default=False, help_text='Diagnóza ve vstupní kontrole')),
                ('deployment_during_diagnosis', models.BooleanField(default=False, help_text='Diagnóza v průběhu hospitalizace')),
                ('deployment_ft_approach', models.BooleanField(default=False, help_text='Vhodnější FT přístup')),
                ('deployment_other_reason', models.TextField(blank=True, help_text='Jiný důvod', null=True)),
                ('discontinuation_contradiction', models.BooleanField(default=False, help_text='Kontraindikace')),
                ('discontinuation_adverse_effect', models.BooleanField(default=False, help_text='Projev nežádoucího účinku')),
                ('discontinuation_adverse_effect_risk', models.BooleanField(default=False, help_text='Riziko nežádoucího účinku')),
                ('discontinuation_missing_indication', models.BooleanField(default=False, help_text='Chybějící indikace')),
                ('discontinuation_allergies', models.BooleanField(default=False, help_text='Alergie')),
                ('discontinuation_drug_interaction', models.BooleanField(default=False, help_text='Léková interakce')),
                ('discontinuation_duplicity', models.BooleanField(default=False, help_text='Duplicity')),
                ('discontinuation_renal_insufficiency', models.BooleanField(default=False, help_text='Renální insuficience')),
                ('discontinuation_hepatic_insufficiency', models.BooleanField(default=False, help_text='Hepatální insuficience')),
                ('discontinuation_medical_intervention', models.BooleanField(default=False, help_text='Lékařská intervence')),
                ('discontinuation_underdosage', models.BooleanField(default=False, help_text='Poddávkování')),
                ('discontinuation_underdosage_risk', models.BooleanField(default=False, help_text='Rizika poddávkováí')),
                ('discontinuation_other_reason', models.TextField(blank=True, help_text='Jiný důvod', null=True)),
                ('dose_change_adverse_effect', models.BooleanField(default=False, help_text='Projev nežádoucího účinku')),
                ('dose_change_adverse_effect_risk', models.BooleanField(default=False, help_text='Riziko nežádoucího účinku')),
                ('dose_change_renal_insufficiency', models.BooleanField(default=False, help_text='Hepatální insuficience')),
                ('dose_change_hepatic_insufficiency', models.BooleanField(default=False, help_text='Renální insuficience')),
                ('dose_change_drug_interaction', models.BooleanField(default=False, help_text='Léková interakce')),
                ('dose_change_underdosage', models.BooleanField(default=False, help_text='Poddávkování')),
                ('dose_change_overdosage', models.BooleanField(default=False, help_text='Předávkování')),
                ('dose_change_laboratory_findings', models.BooleanField(default=False, help_text='Na základě laboratorních výseldků')),
                ('dose_change_dosage_reduction', models.BooleanField(default=False, help_text='Snížení dávky')),
                ('dose_change_dosage_increase', models.BooleanField(default=False, help_text='Zvýšení dávky')),
                ('dose_change_other_reason', models.TextField(blank=True, help_text='Jiný důvod', null=True)),
                ('continuation_drug_reintroduction', models.BooleanField(default=False, help_text='Znovunasazení léčiva')),
                ('continuation_medical_intervention', models.BooleanField(default=False, help_text='Po lékařské intervenci')),
                ('continuation_other_reason', models.TextField(blank=True, help_text='Jiný důvod', null=True)),
                ('tdm_interpretation', models.BooleanField(default=False, help_text='TDM - Interpretace')),
                ('tdm_measure_level_recommendation', models.BooleanField(default=False, help_text='TDM - Doporučení změření hladiny')),
                ('specific_adverse_effect_diagnosis', models.BooleanField(default=False, help_text='Specifika - Diagnostika nežádoucího účinku')),
                ('specific_adverse_effect_reporting', models.BooleanField(default=False, help_text='Specifika - Hlášení nežádoucího účinku')),
                ('specific_consultation', models.BooleanField(default=False, help_text='Specifika - Konzultace')),
                ('recommended_investigation_by_specialist', models.BooleanField(default=False, help_text='Doporučené vyšetření - Specialistou')),
                ('recommended_investigation_by_laboratory', models.BooleanField(default=False, help_text='Doporučené vyšetření - Laboratoří')),
                ('recommended_investigation_by_physical', models.BooleanField(default=False, help_text='Doporučené vyšetření - Fyzikální')),
                ('dosage_determination', models.TextField(blank=True, help_text='Stanovení dávky (při zahájení terapie)', null=True)),
                ('administration_method_optimization', models.TextField(blank=True, help_text='Optimalizace způsobu poddání', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PharmacologicalPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('text', models.TextField(blank=True, help_text='Text farmakologického plánu', null=True)),
                ('his_text', models.TextField(blank=True, help_text='UNIS text', null=True)),
                ('note', models.TextField(blank=True, help_text='Poznámka', null=True)),
                ('notification_datetime', models.DateTimeField(blank=True, help_text='Datum pro upozornění', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PharmacologicalPlanComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('comment_type', models.CharField(choices=[('comment', 'Comment'), ('verification', 'Verification')], default='comment', max_length=20)),
                ('text', models.TextField(blank=True, help_text='Text', null=True)),
                ('verify', models.BooleanField(default=False, help_text='Vykázat ověření')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RiskDrugHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('has_risk_drug', models.BooleanField(default=False, help_text='Rizikové léčivo')),
                ('has_risk_diagnosis', models.BooleanField(default=False, help_text='Riziková diagnóza')),
                ('care', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ipharm.care')),
            ],
            options={
                'verbose_name_plural': 'Risk drug histories',
            },
        ),
        migrations.CreateModel(
            name='RiskDrugHistoryComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('text', models.TextField(help_text='Komentář')),
                ('risk_drug_history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipharm.riskdrughistory')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
