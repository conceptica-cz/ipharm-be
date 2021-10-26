# Generated by Django 3.2.8 on 2021-10-26 11:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('references', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalclinic',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='clinic',
            unique_together={('clinic_type', 'clinic_id')},
        ),
    ]
