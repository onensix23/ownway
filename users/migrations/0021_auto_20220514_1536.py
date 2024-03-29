# Generated by Django 3.2 on 2022-05-14 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0020_usernotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotification',
            name='un_from',
            field=models.ForeignKey(db_column='un_from', default='114', max_length=20, on_delete=django.db.models.deletion.CASCADE, related_name='usernotification_to', to='auth.user', to_field='username'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usernotification',
            name='un_to',
            field=models.ForeignKey(db_column='un_to', default='221', max_length=20, on_delete=django.db.models.deletion.CASCADE, related_name='usernotification_from', to='auth.user', to_field='username'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usernotification',
            name='un_is_sended',
            field=models.BooleanField(default=False),
        ),
    ]
