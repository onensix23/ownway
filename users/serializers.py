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


class UserProfileSerializer2(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
                  'id',
                  'up_id',
                  'up_imagename',
                  'up_comment'
        )
        
class UserSerializer2(serializers.ModelSerializer):
    userprofile_id = UserProfileSerializer2(read_only=True,many=True)

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'email',
                  'userprofile_id', 
        )
        

class UserSerializer3(serializers.ModelSerializer):
    userprofile_id = UserProfileSerializer2(read_only=True,many=True)
    status = serializers.SerializerMethodField('set_status')

    def set_status(self, foo):
        return 'follow'
    
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'email',
                  'userprofile_id', 
                  'status')




class UserFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = (
                  'uf_id',
                  'uf_reader',
                  'uf_reading',
                  )


