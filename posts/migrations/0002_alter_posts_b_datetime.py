# Generated by Django 3.2 on 2021-04-17 19:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='b_datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 17, 19, 31, 28, 870907)),
        ),
    ]
