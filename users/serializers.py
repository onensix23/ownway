import rest_framework.serializers as serializers
from django.contrib.auth.models import User
from .models import *

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
    is_already_follow = serializers.SerializerMethodField('is_already_follow_func')

    def set_status(self, foo):
        return 'follow'
    
    def is_already_follow_func(self, obj):
        user_id = self.context.get("user_id")
        type = self.context.get("type")
        
        if obj.username == user_id:
            return -1
        else:
            if type == 'reader':
                if UserFollow.objects.filter(uf_reader=User.objects.get(username=obj.username), uf_reading=User.objects.get(username=user_id)).exists(): # 내가 이미 리딩 하고 있는 사람이 있는지
                    return True
                else:
                    return False
            elif type == 'reading':
                if UserFollow.objects.filter(uf_reading=User.objects.get(username=obj.username), uf_reader=User.objects.get(username=user_id)).exists(): # 내가 이미 리딩 하고 있는 사람이 있는지
                    return True
                else:
                    return False

    
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'email',
                  'userprofile_id', 
                  'status',
                  'is_already_follow')


class UserFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = (
                  'uf_id',
                  'uf_reader',
                  'uf_reading',
                  )

class UserBlockSerializer(serializers.ModelSerializer):
    ub_from=UserSerializer2(read_only=True)
    ub_to=UserSerializer2(read_only=True)

    class Meta:
        model = UserBlock
        fields = (
                  'ub_id',
                  'ub_from',
                  'ub_to',
                  )

class UserFCMTokenSerializer(serializers.ModelSerializer):
    ufcm_user_id = UserSerializer2(read_only=True)

    class Meta:
        model = UserFCMToken
        fields = (
                  'ufcm_id',
                  'ufcm_user_id',
                  'ufcm_device_id',
                  'ufcm_token',
                  'ufcm_token_check',
                  'ufcm_token_add',
                  'ufcm_sp_c',
                  'ufcm_fu_c',
                  'ufcm_p_c',
                  'ufcm_p_u',
                )

class UserNotificationSerializer(serializers.ModelSerializer):
    usernotification_id=UserFCMTokenSerializer(read_only=True)
    usernotification_from=UserSerializer2(read_only=True)
    usernotification_to=UserSerializer2(read_only=True)

    class Meta:
        model = UserNotification
        fields = (
                  'un_id',
                  'usernotification_id',
                  'un_type',
                  'un_title',
                  'un_body',
                  'usernotification_from',
                  'usernotification_to',
                  'un_send_date',
                  'un_is_sended',
                  'un_is_read',
                  'un_message_id',
                  'un_etc',
                )

class UserNotificationSerializer2(serializers.ModelSerializer):

    class Meta:
        model = UserNotification
        fields = (
                  'un_id',
                  'un_type',
                  'un_title',
                  'un_body',
                  'un_from',
                  'un_to',
                  'un_send_date',
                  'un_is_sended',
                  'un_is_read',
                  'un_message_id',
                  'un_etc',
                )


