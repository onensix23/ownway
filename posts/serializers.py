import rest_framework.serializers as serializers
from .models import Posts, Photo, LikePost, EntrcSido
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
                  'b_locType1',
                  'b_locType2',
                  'b_locType3',
                  'b_theme',
                  'b_title',
                  'b_datetime')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('b_id',
                  'id',
                  'b_locType1',
                  'b_locType2',
                  'b_locType3',
                  'b_theme',
                  'b_title',
                  'b_text',
                  'b_datetime',
                  'p_id')


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('p_id','p_filename','p_image')


class PostDetailSerializer(serializers.ModelSerializer):
    #post_id = serializers.PrimaryKeyRelatedField(queryset=Posts.objects.all(),  many=True)
    #user_id = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), write_only=True, many=False)
    p_id = PhotoSerializer(read_only=True)
    id = UserSerializer(read_only=True)
    class Meta:
        model = Posts
        fields = ('b_id',
                  'id',
                  'b_locType1',
                  'b_locType2',
                  'b_locType3',
                  'b_theme',
                  'b_title',
                  'b_text',
                  'b_datetime',
                  'p_id')


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


