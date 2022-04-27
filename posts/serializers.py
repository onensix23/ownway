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


class PostListSerializer(serializers.ModelSerializer):
    id = UserSerializer(read_only=True)

    class Meta:
        model = Posts
        fields = ('b_id',
                  'id',
                  'b_loctype1',
                  'b_loctype2',
                  'b_loctype3',
                  'b_theme',
                  'b_title',
                  'b_datetime',
                  'b_views',
                #   'p_id'
                )



class PhotoSerializer(serializers.ModelSerializer):
    # photo_b_id = PostListSerializer(read_only=True)

    class Meta:
        model = Photo
        fields = "__all__"
        # fields = ('p_id','p_filename','p_image', 'b_id', 'p_isthumb')


class PostCommentSerializer(serializers.ModelSerializer):
    id = UserSerializer2(read_only=True)

    class Meta:
        model = PostComment
        # fields = "__all__"
        fields = ('pc_id',
                  'b_id',
                  'id',
                  'pc_comment',
                  'pc_datetime',
                  'pc_del'
                  )

class SavePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavePost
        # fields = "__all__"
        fields = ('sp_id',
                  'b_id',
                  'id',
                  'sp_datetime',
                #   'pc_datetime',
                #   'pc_del'
                  )


class PostPlaceSerializer(serializers.ModelSerializer):
    # id = UserSerializer(read_only=True)
    class Meta:
        model = PostPlace
        fields = ('pp_id',
                  'pp_place_id',
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


