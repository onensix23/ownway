# Generated by Django 3.2.13 on 2022-07-12 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0034_auto_20220712_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfcmtoken',
            name='ufcm_pc_u',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
