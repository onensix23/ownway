from datetime import datetime
from django.db import models
from uuid import uuid4

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Posts(models.Model):
    b_id = models.AutoField(primary_key=True)   #게시물 번호
    user_id = models.CharField(max_length=12, null=False)  # 작성자
    b_locType1 = models.CharField(max_length=12, null=False, default='')  # 시
    b_locType2 = models.CharField(max_length=12, null=False, default='')  # 구군
    b_locType3 = models.CharField(max_length=12, null=True, default='')  # 동
    b_theme = models.CharField(max_length=12, null=True, default='') #장소 테마
    b_title = models.CharField(max_length=15, null=False)  # 제목
    b_text = models.TextField()  # 내용
    b_datetime = models.DateTimeField(default=datetime.now, null=False)  # 날짜


    def __str__(self):
        return self.b_title


class Photo(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=False)
    #image = models.ImageField(upload_to='images/', blank=False, null=False)
    image = ProcessedImageField(
        upload_to='images/'+datetime.now().strftime('%Y%m%d')+'/',
        processors=[ResizeToFill(600,600)],
        format='JPEG',
        options={'quality': 90}
    )
    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')

    def get_file_path(instance, filename):
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['media/images/', ymd_path, '/', uuid_name])


class KoreaDongPgTbl(models.Model):
    adm_dr_cd = models.CharField(primary_key=True, max_length=7)
    sido_nm = models.CharField(max_length=45)
    sigungu_nm = models.CharField(max_length=45)
    adm_dr_nm = models.CharField(max_length=45)
    sido_nm_eng = models.CharField(max_length=45, blank=True, null=True)
    sigungu_nm_eng = models.CharField(max_length=45, blank=True, null=True)
    adm_dr_nm_eng = models.CharField(max_length=45, blank=True, null=True)
    sido_nm_cn = models.CharField(max_length=45, blank=True, null=True)
    sigungu_nm_cn = models.CharField(max_length=45, blank=True, null=True)
    adm_dr_nm_cn = models.CharField(max_length=45, blank=True, null=True)
    sido_cd = models.CharField(max_length=2)
    sigungu_cd = models.CharField(max_length=5)
    adm_dr_cd2 = models.CharField(max_length=11)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'korea_dong_pg_tbl'


class EntrcSido(models.Model):
    doro_cd = models.CharField(primary_key=True, max_length=12)
    doro_nm = models.CharField(max_length=80, blank=True, null=True)
    doro_roma = models.CharField(max_length=80, blank=True, null=True)
    dong_one_cd = models.CharField(max_length=2)
    sido_nm = models.CharField(max_length=40, blank=True, null=True)
    sido_roma = models.CharField(max_length=40, blank=True, null=True)
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