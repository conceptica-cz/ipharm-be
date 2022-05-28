# Generated by Django 3.2.13 on 2022-05-28 11:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0003_udpate_url_parameters'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmodelupdate',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modelupdate',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
