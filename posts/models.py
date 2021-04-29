from datetime import datetime
from django.utils import timezone
from django.db import models
from django.utils.timezone import now
from uuid import uuid4



class Posts(models.Model):
    b_id = models.AutoField(primary_key=True)   #게시물 번호
    user_id = models.CharField(max_length=12, null=False)  # 작성자
    b_title = models.CharField(max_length=15, null=False)  # 제목
    b_text = models.TextField()  # 내용
    b_datetime = models.DateTimeField(default=datetime.now, null=False)  # 날짜


    def __str__(self):
        return self.b_title

class Photo(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to='images/', blank=False, null=False)
    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')

    def get_file_path(instance, filename):
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['media/images/', ymd_path, uuid_name])
