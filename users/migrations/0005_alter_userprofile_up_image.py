# Generated by Django 3.2 on 2022-03-20 16:38

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_userprofile_up_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='up_image',
            field=imagekit.models.fields.ProcessedImageField(default='', upload_to='images/profile/20220320/'),
        ),
    ]
