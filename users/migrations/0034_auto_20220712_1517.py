# Generated by Django 3.2.13 on 2022-07-12 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_auto_20220712_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfcmtoken',
            name='ufcm_fu_c',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='userfcmtoken',
            name='ufcm_im_c',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='userfcmtoken',
            name='ufcm_pc_c',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='userfcmtoken',
            name='ufcm_pp_c',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='userfcmtoken',
            name='ufcm_sp_c',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
