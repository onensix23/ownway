# Generated by Django 3.2.13 on 2022-07-12 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_alter_usernoticount_unc_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfcmtoken',
            old_name='ufcm_p_c',
            new_name='ufcm_im_c',
        ),
        migrations.RenameField(
            model_name='userfcmtoken',
            old_name='ufcm_p_u',
            new_name='ufcm_pc_c',
        ),
        migrations.AddField(
            model_name='userfcmtoken',
            name='ufcm_pp_c',
            field=models.CharField(default=1, max_length=1),
        ),
    ]
