import rest_framework.serializers as serializers
from django.contrib.auth.models import User
from .models import *

class ReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = (
            'rt_id',
            'rt_text',
        )
