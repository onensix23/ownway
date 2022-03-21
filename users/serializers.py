import rest_framework.serializers as serializers
from django.contrib.auth.models import User
from .models import UserProfile, UserFollow


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'email')


class UserFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = (
                  'uf_id',
                  'uf_reader',
                  'uf_reading',
                  )


class UserProfileSerializer(serializers.ModelSerializer):
    up_id = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = (
                  'id',
                  'up_id',
                  'up_imagename',
                  'up_comment'
                  )