# Generated by Django 3.2 on 2022-03-13 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_auto_20220313_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='p_filename',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
