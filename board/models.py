from django.db import models
from django.utils.timezone import now


class Board(models.Model):
    b_id = models.AutoField(primary_key=True)   #게시물 번호
    m_id = models.CharField(max_length=12, null=False)  # 작성자
    b_title = models.CharField(max_length=200, null=False)  # 제목
    b_text = models.TextField()  # 내용
    b_datetime = models.DateField(default=now, null=False)  # 날짜
    b_like = models.IntegerField(default=0)  # 좋아요
