# Generated by Django 3.2 on 2022-06-12 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_auto_20220612_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporttemplate',
            name='rt_type',
        ),
    ]
