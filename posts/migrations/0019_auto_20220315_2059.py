# Generated by Django 3.2 on 2022-03-15 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_auto_20220315_1838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='b_latitude',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='b_longtitude',
        ),
    ]
