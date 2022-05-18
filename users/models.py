from datetime import datetime
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from notis.models import *

class UserProfile(models.Model):
    up_id = models.ForeignKey(User, to_field="username", db_column='up_id',related_name='userprofile_id', on_delete=models.CASCADE, max_length=20, null=False)  # 작성자
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


class UserFCMToken(models.Model):
    ufcm_id = models.BigAutoField(primary_key=True)
    ufcm_user_id = models.ForeignKey(User, to_field="username", db_column='ufcm_user_id',related_name='userfcmtoken_id', on_delete=models.CASCADE, max_length=20, null=False)
    ufcm_device_id = models.CharField(max_length=200, null=False)
    ufcm_token = models.CharField(max_length=200, null=True)
    ufcm_token_check = models.DateTimeField(default=datetime.now)
    ufcm_token_add = models.DateTimeField(default=datetime.now)
    ufcm_sp_c = models.CharField(max_length=1, null=False, default=1)
    ufcm_fu_c = models.CharField(max_length=1, null=False, default=1)
    ufcm_p_c = models.CharField(max_length=1, null=False, default=1)
    ufcm_p_u = models.CharField(max_length=1, null=False, default=1)
    

class UserNotification(models.Model):
    un_id = models.BigAutoField(primary_key=True)
    un_token_id = models.ForeignKey(UserFCMToken, to_field="ufcm_id", db_column='un_token_id',related_name='usernotification_id', on_delete=models.CASCADE, max_length=20, null=False)
    un_type = models.ForeignKey(NotiTemplate, to_field="notitemp_type", db_column='un_type',related_name='usernotification_type', on_delete=models.CASCADE, max_length=10, null=False)
    un_title = models.CharField(max_length=200, null=True)
    un_body = models.TextField(null=True)
    un_from = models.ForeignKey(User, to_field="username", db_column='un_from',related_name='usernotification_from', on_delete=models.CASCADE, max_length=20, null=False)
    un_to = models.ForeignKey(User, to_field="username", db_column='un_to',related_name='usernotification_to', on_delete=models.CASCADE, max_length=20, null=False)
    un_send_date = models.DateTimeField(default=datetime.now)
    un_is_sended = models.BooleanField(default=False, null=False)
    un_is_read = models.BooleanField(default=False, null=False)
    un_message_id = models.CharField(max_length=25, null=True)
    un_etc = models.CharField(max_length=100, null=True)

