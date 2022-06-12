from datetime import datetime
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

from posts.models import *

class ReportTemplate(models.Model):
    rt_id = models.BigAutoField(primary_key=True)
    # rt_type = models.CharField(max_length=20,  null=False) # u p c i
    rt_text = models.CharField(max_length=100, null=False)
    rt_is_used = models.BooleanField(default=True)

class Report(models.Model):
    r_id = models.BigAutoField(primary_key=True)

    r_type = models.ForeignKey(ReportTemplate, to_field="rt_id", db_column='r_type',related_name='r_type', on_delete=models.CASCADE, max_length=20, null=False)
    r_typetitle = models.CharField(max_length=20, null=True)

    r_from = models.ForeignKey(User,to_field="username", db_column='r_from', related_name='r_from', null=True, blank=True, on_delete=models.CASCADE)
    r_to = models.ForeignKey(User,to_field="username", db_column='r_to', related_name='r_to', null=True, blank=True, on_delete=models.CASCADE)
    
    r_b_id = models.ForeignKey(Posts,to_field="b_id", db_column='r_b_id', related_name='r_b_id', null=True, blank=True, on_delete=models.CASCADE)
    r_pc_id = models.ForeignKey(PostComment,to_field="pc_id", db_column='r_pc_id', related_name='r_pc_id', null=True, blank=True, on_delete=models.CASCADE)
    r_p_id = models.ForeignKey(Photo,to_field="p_id", db_column='r_p_id', related_name='r_p_id', null=True, blank=True, on_delete=models.CASCADE)
    r_pp_id = models.ForeignKey(PostPlace,to_field="pp_id", db_column='r_pp_id', related_name='r_pp_id', null=True, blank=True, on_delete=models.CASCADE)

    r_report_text = models.TextField(null=True)
    r_is_resolved = models.BooleanField(default=False)
    r_datetime = models.DateTimeField(default=datetime.now)


# insert into reports_reporttemplate(rt_text, rt_type)
# values ('스팸', 'user'),('나체 이미지 또는 성적 행위', 'user'),('혐오 발언 또는 상징', 'user'),('폭력 또는 위험한 단체', 'user'),
# ('불법 또는 규제 상품 판매', 'user'),('따돌림 또는 괴롭힘', 'user'),('지적재산권 침해', 'user'),('거짓 정보', 'user'),
# ('자살, 자해 및 섭식 장애', 'user'),('마음에 들지 않습니다', 'user'),('기타 문제', 'user'),
# ('스팸', 'post'),('나체 이미지 또는 성적 행위', 'post'),('혐오 발언 또는 상징', 'post'),('폭력 또는 위험한 단체', 'post'),
# ('불법 또는 규제 상품 판매', 'post'),('따돌림 또는 괴롭힘', 'post'),('지적재산권 침해', 'post'),('거짓 정보', 'post'),
# ('자살, 자해 및 섭식 장애', 'post'),('마음에 들지 않습니다', 'post'),('기타 문제', 'post'),
# ('스팸', 'comment'),('나체 이미지 또는 성적 행위', 'comment'),('혐오 발언 또는 상징', 'comment'),('폭력 또는 위험한 단체', 'comment'),
# ('불법 또는 규제 상품 판매', 'comment'),('따돌림 또는 괴롭힘', 'comment'),('지적재산권 침해', 'comment'),('거짓 정보', 'comment'),
# ('자살, 자해 및 섭식 장애', 'comment'),('마음에 들지 않습니다', 'comment'),('기타 문제', 'comment');
