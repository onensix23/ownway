# Generated by Django 3.2 on 2021-04-20 21:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_posts_b_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='b_datetime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
