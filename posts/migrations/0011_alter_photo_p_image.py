# Generated by Django 3.2 on 2022-03-08 15:21

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_alter_photo_p_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='p_image',
            field=imagekit.models.fields.ProcessedImageField(default='', upload_to='images/20220308/'),
        ),
    ]
