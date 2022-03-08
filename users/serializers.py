import rest_framework.serializers as serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
                    'username',
                    'firstname'
                  )


class UserProfileSerializer(serializers.ModelSerializer):
    id = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = (
                  'up_id',
                  'up_image',
                  'up_imagename',
                  'up_comment'
                  )