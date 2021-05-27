import rest_framework.serializers as serializers
from .models import Posts


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('b_id',)