import rest_framework.serializers as serializers
from .models import *
from users.serializers import UserSerializer2
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # userprofile_id = UserProfileSerializer2(read_only=True)
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'email')


class PhotoSerializer(serializers.ModelSerializer):
    p_user_id = UserSerializer2(read_only=True)

    class Meta:
        model = Photo
        fields = ('p_id',
                  'p_filename',
                  'p_datetime', 
                  'p_isthumb',
                  'p_is_reported',
                  'p_user_id')


class PostCommentSerializer(serializers.ModelSerializer):
    id = UserSerializer2(read_only=True)

    class Meta:
        model = PostComment
        fields = ('pc_id',
                  'b_id',
                  'id',
                  'pc_comment',
                  'pc_datetime',
                  'pc_type',
                  'pc_etc',
                  'pc_del',
                  
                  )


class PostCommentSerializer2(serializers.ModelSerializer):
    # id = UserSerializer2(read_only=True)

    class Meta:
        model = PostComment
        # fields = "__all__"
        fields = (
                  'b_id',
                  )

class SavePostSerializer(serializers.ModelSerializer):
    savepost_username = UserSerializer2(read_only=True)
    
    class Meta:
        model = SavePost
        # fields = "__all__"
        fields = ('sp_id',
                  'savepost_username',
                  'id',
                  'sp_datetime',
                  'sp_is_noti',
                #   'pc_datetime',
                #   'pc_del'
                  )
       
        
class CountUnreadSerializer(serializers.ModelSerializer):
    # countunread_sp_id = SavePostSerializer(read_only=True)
    class Meta:
        model = CountUnread
        # fields = "__all__"
        fields = ('cu_id',
                  'cu_pre_datetime',
                  'cu_datetime',
                  'cu_count'
                #   'pc_datetime',
                #   'pc_del'
                  )
        
class SavePostSerializer2(serializers.ModelSerializer):
    # savepost_username = UserSerializer2(read_only=True)
    countunread_sp_id = CountUnreadSerializer(read_only=True, many=True)
    
    class Meta:
        model = SavePost
        # fields = "__all__"
        fields = ('sp_id',
                #   'savepost_username',
                  'countunread_sp_id',
                  'id',
                  'sp_datetime',
                  'sp_is_noti',
                #   'pc_datetime',
                #   'pc_del'
                  )




class PostPlaceSerializer(serializers.ModelSerializer):
    pp_user_id = UserSerializer2(read_only=True)
    class Meta:
        model = PostPlace
        fields = ('pp_id',
                  'pp_place_id',
                  'pp_user_id',
                  'pp_datetime',
                  'pp_type',
                  'pp_del',
                )


class PostSerializer(serializers.ModelSerializer):
    savepost_b_id = SavePostSerializer(read_only=True , many=True)
    photo_b_id = PhotoSerializer(read_only=True, many=True)
    postcomment_b_id = PostCommentSerializer(read_only=True, many=True)
    postplace_b_id = PostPlaceSerializer(read_only=True, many=True)
    id = UserSerializer2(read_only=True)
    
    class Meta:
        model = Posts
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    photo_b_id = PhotoSerializer(read_only=True, many=True)
    savepost_b_id = SavePostSerializer(read_only=True , many=True)
    id = UserSerializer2(read_only=True)
    
    class Meta:
        model = Posts
        fields = "__all__"
        
class PostListSerializer2(serializers.ModelSerializer):
    photo_b_id = PhotoSerializer(read_only=True , many=True)
    savepost_b_id = SavePostSerializer(read_only=True , many=True)
    id = UserSerializer2(read_only=True)
    CountUnreadSerializer = CountUnreadSerializer(read_only=True , many=True)
    
    class Meta:
        model = Posts
        fields = "__all__"
        
class PostDetailSerializer(serializers.ModelSerializer):
    # p_id = PhotoSerializer(read_only=True)
    id = UserSerializer2()

    class Meta:
        model = Posts
        fields = "__all__"
        # fields = ('b_id',
        #           'id',
        #           'b_loctype1',
        #           'b_loctype2',
        #           'b_loctype3',
        #           'b_theme',
        #           'b_title',
        #           'b_datetime',
        #           'b_views',
        #         )


class LikePostSerializer(serializers.ModelSerializer):
    id = UserSerializer(read_only=True)
    b_id = PostSerializer(read_only=True)

    class Meta:
        model = Posts
        fields = ('lp_id',
                  'lp_datetime',
                  'id',
                  'b_id',
                  'lp_del',
                  )


class IsLikePostSerializer(serializers.ModelSerializer):
    id = UserSerializer(read_only=True)
    b_id = PostSerializer(read_only=True)

    class Meta:
        model = LikePost
        fields = ('lp_id',
                  'lp_datetime',
                  'id',
                  'b_id',
                  'lp_del',
                  )


class EntrcSidoFirstSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrcSido
        fields = (
                  'sido_cd',
                  'sido_nm',
                  )


class EntrcSidoSecondSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrcSido
        fields = (
                  'sigungu_cd',
                  'sigungu_nm',
                  )


class EntrcSidoThirdSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrcSido
        fields = (
                  'dong_cd',
                  'dong_nm',
                  )

class EntrcSidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrcSido
        fields = ('doro_cd',
                  'doro_nm',
                  'sido_cd',
                  'sido_nm',
                  'sigungu_cd',
                  'sigungu_nm',
                  'dong_cd',
                  'dong_nm',
                  )


