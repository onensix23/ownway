# Generated by Django 3.2 on 2022-05-20 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0029_savepost_sp_is_noti'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savepost',
            name='sp_is_noti',
            field=models.BooleanField(default=True),
        ),
    ]
