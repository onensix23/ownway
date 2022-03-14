import rest_framework.serializers as serializers
from .models import Posts, Photo, LikePost, EntrcSido, PostComment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
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
        # fields = "__all__"
        fields = ('p_id','p_filename','p_image', 'b_id', 'p_isthumb')



class PostSerializer(serializers.ModelSerializer):
    # p_id = PhotoSerializer(read_only=True)
    photo_b_id = PhotoSerializer(read_only=True, many=True)
    id = UserSerializer(read_only=True)
    
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
        #         #   'b_text',
        #           'b_datetime',
        #           'b_views',
        #         #   'p_id'
        #             )


class PostDetailSerializer(serializers.ModelSerializer):
    # p_id = PhotoSerializer(read_only=True)
    id = UserSerializer()

    class Meta:
        model = Posts
        fields = ('b_id',
                  'id',
                  'b_loctype1',
                  'b_loctype2',
                  'b_loctype3',
                  'b_theme',
                  'b_title',
                #   'b_text',
                  'b_datetime',
                  'b_views',
                #   'p_id'
                  )


class PostCommentSerializer(serializers.ModelSerializer):
    id = UserSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = ('pc_id',
                  'b_id',
                  'id',
                  'pc_comment',
                  'pc_datetime',
                  'pc_del'
                  )


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


