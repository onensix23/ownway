# Generated by Django 3.2 on 2022-06-12 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0030_alter_savepost_sp_is_noti'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='p_is_reported',
            field=models.BooleanField(default=False),
        ),
    ]
