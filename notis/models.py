from datetime import datetime
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

class NotiTemplate(models.Model):
    notitemp_type = models.CharField(max_length=10, null=False, primary_key=True)
    notitemp_title =  models.CharField(max_length=200, null=True)
    notitemp_body = models.TextField(null=True)
    notitemp_datetime  = models.DateTimeField(default=datetime.now)
