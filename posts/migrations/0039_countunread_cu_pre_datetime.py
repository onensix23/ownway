# Generated by Django 3.2.13 on 2022-08-08 13:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0038_countunread'),
    ]

    operations = [
        migrations.AddField(
            model_name='countunread',
            name='cu_pre_datetime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
