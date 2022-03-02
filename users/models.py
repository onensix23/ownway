from datetime import datetime
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# Create your models here.

class UserProfile(models.Model):
    up_id = models.ForeignKey(User, to_field="username", db_column='up_id', on_delete=models.CASCADE, unique=True, max_length=12, null=False)  # 작성자
    up_image = ProcessedImageField(
        null=False, default='',
        upload_to='images/'+datetime.now().strftime('%Y%m%d')+'/',
        processors=[ResizeToFill(600,600)],
        format='JPEG',
        options={'quality': 90}
    )
    up_imagename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')
    up_comment = models.CharField(max_length=15, null=True)


class User(models.Model):
    user_id = models.CharField(max_length=20, verbose_name='아이디')
    user_email = models.CharField(null=True, max_length=30, verbose_name='이메일')
    user_nickname = models.CharField(max_length=20, verbose_name='닉네임')
    user_password = models.CharField(max_length=35, verbose_name='비밀번호')

    def __str__(self):  # 이 함수 추가
        return self.username  # User object 대신 나타낼 문자
