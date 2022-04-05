from datetime import datetime
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Posts(models.Model):
    b_id = models.AutoField(primary_key=True)
    id = models.ForeignKey(User, to_field="username", db_column='id', default='', on_delete=models.CASCADE, max_length=12, null=False) 
    b_address = models.CharField(max_length=100, null=False, default='') 
    b_theme = models.CharField(max_length=12, null=True, default='') 
    b_hash_tag_1 = models.CharField(max_length=50, null=True, default='') 
    b_hash_tag_2 = models.CharField(max_length=50, null=True, default='') 
    b_views = models.CharField(max_length=12, null=True, default='0') 
    b_title = models.CharField(max_length=15, null=True) 
    b_place_id = models.TextField(null=True)
    b_datetime = models.DateTimeField(default=datetime.now, null=False)
    b_del = models.CharField(max_length=1, null=False, default='N')

    def __str__(self):
        return self.b_title


class Photo(models.Model):
    p_id = models.BigAutoField(primary_key=True)
    b_id  = models.ForeignKey(Posts, db_column='b_id', related_name='photo_b_id',default='', max_length=12, null=False, blank=True, on_delete=models.CASCADE)
    p_filename = models.CharField(max_length=256, null=True)
    p_isthumb = models.CharField(max_length=2,null=False,  default='0')
    p_datetime = models.DateTimeField(default=datetime.now)  # 날짜

    def get_file_path(instance, filename):
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['media/images/', ymd_path, '/', uuid_name])


class LikePost(models.Model):
    lp_id = models.BigAutoField(primary_key=True)
    id = models.ForeignKey(User, to_field="username", db_column='id', default='', on_delete=models.CASCADE,
                           max_length=12, null=False)  # 작성자
    b_id = models.ForeignKey(Posts, db_column='b_id', on_delete=models.CASCADE, null=False)
    lp_datetime = models.DateTimeField(default=datetime.now, null=False)  # 날짜
    lp_del = models.CharField(max_length=1, null=False, default='N')


class SavePost(models.Model):
    sp_id = models.BigAutoField(primary_key=True)
    id = models.ForeignKey(User, to_field="username",
                                related_name='savepost_username',
                                db_column='id', default='', on_delete=models.CASCADE,
                           max_length=12, null=False)  # 작성자
    b_id = models.ForeignKey(Posts, db_column='b_id', 
                                related_name='savepost_b_id',
                                on_delete=models.CASCADE, null=False)
    sp_datetime = models.DateTimeField(default=datetime.now, null=False)  # 날짜
    # lp_del = models.CharField(max_length=1, null=False, default='N')


class PostComment(models.Model):
    pc_id = models.BigAutoField(primary_key=True)
    b_id = models.ForeignKey(Posts, db_column='b_id', related_name='postcomment_b_id', on_delete=models.CASCADE, null=False)
    id = models.ForeignKey(User, to_field="username", db_column='id', default='', on_delete=models.CASCADE,
                           max_length=12, null=False)  # 작성자
    pc_comment = models.TextField()  # 내용
    pc_datetime = models.DateTimeField(default=datetime.now, null=False)  # 날짜
    pc_type = models.CharField(max_length=2, null=False, default='0' )
    pc_del = models.CharField(max_length=1, null=False, default='N')


class PostPlace(models.Model):
    pp_id = models.BigAutoField(primary_key=True)
    b_id = models.ForeignKey(Posts, db_column='b_id', related_name='postplace_b_id', on_delete=models.CASCADE, null=False)
    id = models.ForeignKey(User, to_field="username", db_column='id', default='', on_delete=models.CASCADE,
                           max_length=12, null=False)  # 작성자
    pp_place_id = models.TextField()  # 내용
    pp_datetime = models.DateTimeField(default=datetime.now, null=False)  # 날짜
    pp_type = models.CharField(max_length=2, null=False, default='0' )
    pp_del = models.CharField(max_length=1, null=False, default='N')


class EntrcSido(models.Model):
    doro_cd = models.CharField(primary_key=True, max_length=12)
    doro_nm = models.CharField(max_length=80, blank=True, null=True)
    doro_roma = models.CharField(max_length=80, blank=True, null=True)
    dong_one_cd = models.CharField(max_length=2)
    sido_cd = models.CharField(max_length=40, blank=True, null=True)
    sido_nm = models.CharField(max_length=40, blank=True, null=True)
    sido_roma = models.CharField(max_length=40, blank=True, null=True)
    sigungu_cd = models.CharField(max_length=40, blank=True, null=True)
    sigungu_nm = models.CharField(max_length=40, blank=True, null=True)
    sigungu_roma = models.CharField(max_length=40, blank=True, null=True)
    dong_nm = models.CharField(max_length=40, blank=True, null=True)
    dong_roma = models.CharField(max_length=40, blank=True, null=True)
    dong_type = models.CharField(max_length=1, blank=True, null=True)
    dong_cd = models.CharField(max_length=3, blank=True, null=True)
    is_use = models.CharField(max_length=1, blank=True, null=True)
    change_reason = models.CharField(max_length=1, blank=True, null=True)
    change_content = models.CharField(max_length=14, blank=True, null=True)
    from_date = models.CharField(max_length=8, blank=True, null=True)
    to_date = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entrc_sido'
        unique_together = (('doro_cd', 'dong_one_cd'),)