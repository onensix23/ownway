from datetime import datetime
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

class UserProfile(models.Model):
    up_id = models.ForeignKey(User, to_field="username", db_column='up_id', on_delete=models.CASCADE, max_length=20, null=False)  # 작성자
    up_imagename = models.CharField(max_length=256, null=True, verbose_name='첨부파일명')
    up_comment = models.CharField(max_length=15, null=True)


class UserFollow(models.Model):
    uf_id = models.BigAutoField(primary_key=True)
    uf_reader = models.ForeignKey(User, to_field="username", 
                related_name='reader',
                db_column='uf_reader', on_delete=models.CASCADE, max_length=12, null=False)  # 팔로워
    uf_reading =  models.ForeignKey(User, to_field="username", 
                related_name='reading',
                db_column='uf_reading', on_delete=models.CASCADE, max_length=12, null=False)  # 팔로잉
