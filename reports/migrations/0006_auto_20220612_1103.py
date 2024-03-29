# Generated by Django 3.2 on 2022-06-12 11:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0005_report_r_typetitle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='r_user_id',
        ),
        migrations.AddField(
            model_name='report',
            name='r_from',
            field=models.ForeignKey(blank=True, db_column='r_from', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_from', to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
        migrations.AddField(
            model_name='report',
            name='r_to',
            field=models.ForeignKey(blank=True, db_column='r_to', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_to', to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]
