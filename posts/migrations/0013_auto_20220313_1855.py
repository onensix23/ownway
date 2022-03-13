# Generated by Django 3.2 on 2022-03-13 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_auto_20220313_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='b_locType1',
            new_name='b_loctype1',
        ),
        migrations.RenameField(
            model_name='posts',
            old_name='b_locType2',
            new_name='b_loctype2',
        ),
        migrations.RenameField(
            model_name='posts',
            old_name='b_locType3',
            new_name='b_loctype3',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='p_id',
        ),
        migrations.AddField(
            model_name='photo',
            name='b_id',
            field=models.ForeignKey(blank=True, db_column='b_id', default='', max_length=12, on_delete=django.db.models.deletion.CASCADE, to='posts.posts'),
        ),
        migrations.AddField(
            model_name='photo',
            name='p_isthumb',
            field=models.CharField(default='0', max_length=2, verbose_name='썸네일 여부(0:false, 1:true)'),
        ),
    ]
