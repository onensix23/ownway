# Generated by Django 3.2 on 2022-06-12 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0032_postcomment_pc_is_reported'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='b_is_reported',
            field=models.BooleanField(default=False),
        ),
    ]
