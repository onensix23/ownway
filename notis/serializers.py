import rest_framework.serializers as serializers
from .models import *

class NotiTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotiTemplate
        fields = ('notitemp_type',
                  'notitemp_title',
                  'notitemp_body',
                  'notitemp_datetime')
