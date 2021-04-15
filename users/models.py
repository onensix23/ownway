from django.db import models
# Create your models here.


class User(models.Model):
    user_id = models.CharField(max_length=20, verbose_name='아이디')
    user_email = models.CharField(null=True, max_length=30, verbose_name='이메일')
    user_nickname = models.CharField(max_length=20, verbose_name='닉네임')
    user_password = models.CharField(max_length=35, verbose_name='비밀번호')

    def __str__(self):  # 이 함수 추가
        return self.username  # User object 대신 나타낼 문자
