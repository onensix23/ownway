from datetime import datetime
from django.utils import timezone
from django.db import models
from django.utils.timezone import now


class Posts(models.Model):
    b_id = models.AutoField(primary_key=True)   #게시물 번호
    user_id = models.CharField(max_length=12, null=False)  # 작성자
    b_title = models.CharField(max_length=15, null=False)  # 제목
    b_text = models.TextField()  # 내용
    b_datetime = models.DateTimeField(default=datetime.now, null=False)  # 날짜
    image = models.ImageField(upload_to="img/")