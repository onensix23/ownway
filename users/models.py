from datetime import datetime
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from notis.models import *
from posts.models import *

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


class UserBlock(models.Model):
    ub_id = models.BigAutoField(primary_key=True)
    ub_from = models.ForeignKey(User, to_field="username", 
                related_name='ub_from',
                db_column='ub_from', on_delete=models.CASCADE, max_length=12, null=False)  # 누가
    ub_to =  models.ForeignKey(User, to_field="username", 
                related_name='ub_to',
                db_column='ub_to', on_delete=models.CASCADE, max_length=12, null=False)  # 누구에게


class UserFCMToken(models.Model):
    ufcm_id = models.BigAutoField(primary_key=True)
    ufcm_user_id = models.ForeignKey(User, to_field="username", db_column='ufcm_user_id',related_name='userfcmtoken_id', on_delete=models.CASCADE, max_length=20, null=False)
    ufcm_device_id = models.CharField(max_length=200, null=False)
    ufcm_token = models.CharField(max_length=200, null=True)
    ufcm_token_check = models.DateTimeField(default=datetime.now)
    ufcm_token_add = models.DateTimeField(default=datetime.now)
    ufcm_sp_c = models.BooleanField(default=True, null=True)
    ufcm_fu_c = models.BooleanField(default=True, null=True)
    ufcm_pc_c = models.BooleanField(default=True, null=True)
    ufcm_pc_u = models.BooleanField(default=True, null=True) #3번은 알림 주는 권한
    ufcm_pp_c = models.BooleanField(default=True, null=True)
    ufcm_im_c = models.BooleanField(default=True, null=True)
    

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
    un_etc = models.ForeignKey(Posts, to_field="b_id", db_column='un_etc',related_name='usernotification_etc', on_delete=models.CASCADE, max_length=10, null=True)
    un_detail_etc = models.CharField(max_length=100, null=True)
    
class UserNotiCount(models.Model):
    unc_id = models.BigAutoField(primary_key=True)
    unc_user_id = models.ForeignKey(User, to_field="username", db_column='unc_user_id',related_name='unc_user_id', on_delete=models.CASCADE, max_length=20, null=False)
    unc_b_id = models.ForeignKey(Posts, to_field="b_id", db_column='unc_b_id',related_name='unc_b_id', on_delete=models.CASCADE, max_length=10, null=True)
    unc_count = models.IntegerField(default=0)
    
