from django.db.models.functions import Substr
from django.shortcuts import render, redirect
from snsP.my_settings import *
from django.http import HttpResponse
from django.db.models import Q,Subquery
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from snsP.storages import FileUpload, s3_client
from .serializers import *
from .models import *
from users.models import UserFollow
import json


class UploadImageViewSet(APIView):
    """
       POST /uploadImage
    """
    def post(self, request, **kwargs):
        res_data = {
            "success": True,
            "error": None,
            "fileName": '',
            "image_cnt":0
        }

        postObj = Posts.objects.get(b_id=request.data['b_id'])

        cnt = 0

        if request.FILES:
            for k in request.FILES.keys():
                if k.find('uploadFile') != -1:
                    cnt = cnt + 1

                    photo = Photo()
                    photo.b_id = postObj
                    photo.p_filename = FileUpload(s3_client).upload(request.FILES[k])
                    photo.p_isthumb = request.data['type']

                    # 데이터베이스에 저장
                    photo.save()

                    res_data[k] = request.FILES[k].name
                    
        res_data['image_cnt'] = cnt
        return Response(res_data, status=200)


class DeleteImageViewSet(APIView):
    """
       POST /deleteImage
    """
    def post(self, request, **kwargs):
        res_data = {
            "success": True,
            "error": None,
            "fileName": '',
            "image_cnt":0
        }
        b_id=request.data['b_id']
        p_id=request.data['p_id']
        p_filename = request.data['p_filename']
        
        print(request.data)

        photoObj = Photo.objects.get(b_id=b_id,p_id=p_id)

        try:
            FileUpload(s3_client).delete(p_filename)
            photoObj.delete()
        except:
            print('except')
            # return Response(res_data, status=200)
        
        return Response(res_data, status=200)



class PostViewSet(APIView):
    """
       POST /savePost
    """
    def post(self, request, **kwargs):

        res_data = {
            'post_success': False,
            'postcomment_success': 'no comment',
            'b_id': 6
        }

        # print(request.data)

        user_id = request.data['user_id']
        b_title = request.data['b_title']
        b_address = request.data['b_address']
        b_theme = request.data['b_theme']
        b_hash_tag_1 = request.data['b_hash_tag_1']
        b_hash_tag_2 = request.data['b_hash_tag_2']
        b_place_id = request.data['b_place_id']

        pc_comment = request.data['pc_comment']

        # print(request.data)

        userObj = User.objects.get(username=user_id)

        new_post = Posts(
                id=userObj, 
                b_title=b_title, 
                b_address=b_address,  
                b_theme=b_theme, 
                b_hash_tag_1=b_hash_tag_1, b_hash_tag_2=b_hash_tag_2, 
        )

        new_post.save()  # insert
        
        res_data['post_success']=True
        
        # print(new_post.b_id)

        res_data['b_id'] = new_post.b_id

        postObj = Posts.objects.get(b_id=new_post.b_id)

        if pc_comment != '':
            new_postcomment = PostComment(
                b_id=postObj,
                id=userObj,
                pc_comment=pc_comment,
                pc_type='1'
            )

            new_postcomment.save()
            res_data['postcomment_success']=True
        
        if b_place_id != '':
            new_postplace = PostPlace(
                b_id=postObj,
                id=userObj,
                pp_place_id = b_place_id,
                pp_type='1',
            )

            new_postplace.save()
            res_data['postplace_success']=True

        return Response(res_data, status=200)

    """
    GET /board
        detail (b_id)
    """
    def get(self, request, **kwargs):
        if(len(request.GET) > 0): #detail
            # print('1')
            get_queryset = Posts.objects.prefetch_related('photo_b_id').prefetch_related('postcomment_b_id').prefetch_related('postplace_b_id').prefetch_related('savepost_b_id').filter(Q(
                Q(b_id=request.GET['b_id'])
            )).select_related('id')
            get_serializer_class = PostSerializer(get_queryset, many=True)

        else:
            # print('2')
            get_queryset = Posts.objects.prefetch_related('photo_b_id').prefetch_related('savepost_b_id').select_related('id').order_by('-b_datetime')

            get_serializer_class = PostSerializer(get_queryset, many=True)

        return Response(get_serializer_class.data, status=200)

    """
        PUT /board/{b_id}
    """
    def put(self, request, **kwargs):
        res_data = {
            "success": True,
            "error": None
        }

        if request.data['v_b_text'] == '990622':
            b_id = request.data['b_id']
            queryset = Posts.objects.get(b_id=b_id)
            queryset.delete()

        else:
            user_id = request.user.get_username()
            user_id = request.data['userId']
            b_id = request.data['b_id']
            b_text = request.data['v_b_text']
            b_title = request.data['v_b_title']

            edit_board1 = Posts.objects.get(b_id=b_id)
            edit_board1.b_title = b_title
            edit_board1.b_text = b_text

            edit_board1.save()

        return Response(res_data, status=200)


class SearchPostViewSet(APIView):
    """
       POST /searchPost
    """

    def post(self, request, **kwargs):

        address = request.data['locationValue']
        type = request.data['themeValue']
        tag = request.data['hashTagValue']
        text = request.data['text']

        print(request.data)
        # get_queryset = Posts.objects.filter(b_title__icontains=text)
        # get_serializer_class = PostDetailSerializer(get_queryset, many=True)

        """
            select * from posts 
            where b_address like '~' & b_type = ''
        """
        get_queryset = Posts.objects

        q = Q()

        if address != '' : 
            q.add(Q(b_address__icontains=address), q.AND)
        if type != '':
            q.add(Q(b_theme__icontains=type), q.AND)
        if tag != '':
            q.add(Q(b_hash_tag_1__icontains=tag),q.OR)
            q.add(Q(b_hash_tag_2__icontains=tag),q.OR)
        if text != '':
            q.add(Q(b_title__icontains=text), q.AND)

        get_queryset = Posts.objects.filter(q).prefetch_related('photo_b_id').prefetch_related('savepost_b_id').select_related('id').order_by('-b_datetime')
        get_serializer_class = PostSerializer(get_queryset, many=True)

        return Response(get_serializer_class.data, status=200)


class LikePostViewSet(APIView):
    """
    GET, POST /likepost/
    """

    def post(self, request, **kwargs):
        res_data = {
            "success": True,
            "error": None,
            "result":''
        }

        # {"type":"0","userId":"1142995766470027","b_id":"10"}
        if request.data['type'] == '0': # 좋아요 눌려있는지 확인
            user_id = request.data['userId']
            b_id = request.data['b_id']
            
            get_queryset = LikePost.objects.filter(id=user_id, b_id=b_id)
            get_serializer_class = IsLikePostSerializer(get_queryset, many=True)

            return Response(get_serializer_class.data, status=200)

        else: # 좋아요 실질적인 데이터 변경
            user_id = request.data['userId']
            b_id = request.data['b_id']

            get_queryset = LikePost.objects.filter(id=user_id, b_id=b_id).count()

            if get_queryset == 0:
                # insert
                sel_post = Posts.objects.get(b_id=b_id)
                sel_user = User.objects.get(username=user_id)

                # new_likepost = LikePost(id=user_id, b_id=b_id)
                LikePost.objects.create(
                    id=sel_user,
                    b_id=sel_post,
                )

                res_data["result"] = 'N'

            else:
                # update
                uLikePost = LikePost.objects.get(id=user_id, b_id=b_id)

                if uLikePost.lp_del == "Y":
                    uLikePost.lp_del = "N"
                    res_data["result"] = 'N'
                else:
                    uLikePost.lp_del = "Y"
                    res_data["result"] = 'Y'

                uLikePost.save()

            return Response(res_data, status=200)


class LikePostMpViewSet(APIView):
    """
        POST /mplikepost/
    """

    def post(self, request, **kwargs):
        res_data = {
            "success": True,
            "error": None
        }
        if request.data['type'] == 0:
            # select
            user_id = request.data['userId']
            get_queryset = LikePost.objects.filter(id=user_id, lp_del='N')

            print(get_queryset)
            print(get_queryset.values_list())

            lp_id_list = []

            for vl in get_queryset.values_list():
                lp_id_list.append(vl[2])

            res_queryset = Posts.objects.filter(b_id__in=lp_id_list)

            get_serializer_class = PostDetailSerializer(res_queryset, many=True)
            print(get_serializer_class.data)
            return Response(get_serializer_class.data, status=200)
            # return  Response({"res": "hi"}, status=200)

class PostCommentViewSet(APIView):
    """
        GET /postcomment/
    """

    def get(self, request, **kwargs):
        b_id = request.GET.get('b_id')
        pc_type = request.GET.get('pc_type')
        get_queryset = PostComment.objects.filter(pc_del='N', b_id=b_id, pc_type=pc_type).order_by('pc_datetime')
        get_serializer_class = PostCommentSerializer(get_queryset, many=True)
        return Response(get_serializer_class.data, status=200)

    """
        POST /postcomment/
    """

    def post(self, request, **kwargs):
        res_data = {
            "success": True,
            "error": None
        }

        # select
        user_id = request.data['userId']
        b_id = request.data['b_id']
        pc_comment = request.data['pc_comment']

        userObj = User.objects.get(username=user_id)
        postId = Posts.objects.get(b_id=b_id)

        new_Comment = PostComment(id=userObj, b_id=postId, pc_comment=pc_comment)
        new_Comment.save()  # insert

        res_data = {
            "success": True,
            "error": None
        }

        return Response(res_data, status=200)


class PostPlaceViewSet(APIView):
    """
    # DELETE /postPlcae/
    # 
    """
    def delete(self, request, pp_id):
        res_data = {
            "success":True
        }
        
        try:
            model = PostPlace.objects.get(pp_id=pp_id)
            model.delete()
        except:
            res_data["success"] = False

        return Response(res_data, status=200)

class SavePostPlaceViewSet(APIView):
    """
        POST /postPlcae/
    """
    def post(self, request, **kwargs):

        res_data = {
            "success": True,
            "error": None
        }

        # select
        user_id = request.data['userId']
        b_id = request.data['b_id']
        pp_place_id = request.data['place_id']

        userObj = User.objects.get(username=user_id)
        postId = Posts.objects.get(b_id=b_id)

        try:
            new_postplace = PostPlace(id=userObj, b_id=postId, pp_place_id=pp_place_id)
            new_postplace.save()  # insert
        except:
            res_data["success"]=False

        return Response(res_data, status=200)

class MyPageViewSet(APIView):
    """
    POST /mypage/
    """

    def post(self, request, **kwargs):
        user_id = request.data['userId']
        get_queryset = Posts.objects.filter(id=user_id, b_del='N').order_by('-b_datetime')
        get_serializer_class = PostSerializer(get_queryset, many=True)
        # print(get_serializer_class.data)
        return Response(get_serializer_class.data, status=200)


class FollowPostViewSet(APIView):
    """
    POST /followPost/
    """
    def post(self, request, **kwargs):
        user_id = request.data['userId']

        get_queryset = Posts.objects.filter(id__in=Subquery(UserFollow.objects.values('uf_reading').filter(uf_reader=user_id)), b_del='N').order_by('-b_datetime')
        get_serializer_class = PostSerializer(get_queryset, many=True)

        return Response(get_serializer_class.data, status=200)


class SavePostViewSet(APIView):
    """
    /savePost
    GET  param userId
    POST param userId, b_id
    """
    def get(self, request, **kwargs):
        user_id = request.GET['userId']

        get_queryset = Posts.objects.filter(b_id__in=Subquery(SavePost.objects.values('b_id').filter(id=user_id))).prefetch_related('photo_b_id').prefetch_related('savepost_b_id').select_related('id').order_by('-b_datetime')
        get_serializer_class = PostSerializer(get_queryset, many=True)

        return Response(get_serializer_class.data, status=200)


    def post(self, request, **kwargs):
        res_data = {
            'action' : 'create',
            'count' : 0,
            "success" : True
        }

        user_id = request.data['userId']
        b_id = request.data['b_id']

        userObj = User.objects.get(username=user_id)
        postObj = Posts.objects.get(b_id=b_id)

        if request.data['type'] == '0':
            query_count = SavePost.objects.filter(id=user_id, b_id=b_id).count()
            if query_count > 0:
                res_data['count'] = query_count
        else:
            savePostObj, isCreated =  SavePost.objects.get_or_create(id=userObj, b_id=postObj)

            if isCreated == False: # 삭제 해야 됨
                res_data['action'] = 'delete'
                savePostObj.delete()

        return Response(res_data, status=200)


class GetSidoViewSet(APIView):
    """
    GET /mypage/
    """

    def get(self, request, **kwargs):
        sido = EntrcSido.objects.values('sido_nm').annotate(sido_cd=(Substr('doro_cd', 1, 2))).distinct()
        sido_list = EntrcSidoFirstSerializer(sido, many=True)  # 시- 도 return
        # print(sido_list)
        return Response(sido_list.data, status=200)


class GetSigunguViewSet(APIView):
    """
    POST /getSigungu
    """

    def post(self, request, **kwargs):
        sel_sido_cd = request.data['sido_cd']

        sigungu = EntrcSido.objects.values('sigungu_nm').annotate(
            sigungu_cd=(Substr('doro_cd', 3, 3))).distinct().filter(sido_cd=sel_sido_cd)

        sigungu_list = EntrcSidoSecondSerializer(sigungu, many=True)  # 시- 도 return
        # print(sido_list)
        return Response(sigungu_list.data, status=200)


class GetDongViewSet(APIView):
    """
    POST /getDong
    """

    def post(self, request, **kwargs):
        sel_sido_cd = request.data['sido_cd']
        sel_sigungu_cd = request.data['sigungu_cd']

        dong = EntrcSido.objects.values('dong_nm', 'dong_cd').distinct().filter(sido_cd=sel_sido_cd,
                                                                                sigungu_cd=sel_sigungu_cd).exclude(
            dong_nm__exact='')

        print(dong)
        dong_list = EntrcSidoThirdSerializer(dong, many=True)  # 시- 도 return

        return Response(dong_list.data, status=200)


class GetReSidoViewSet(APIView):
    """
    POST /mypage/
    """

    def post(self, request, **kwargs):
        # { "sido_nm":"경기도" }
        sel_sido_nm = request.data['sido_nm']
        print(sel_sido_nm)
        sido = EntrcSido.objects.values('sido_cd', 'sido_nm').filter(sido_nm=sel_sido_nm).distinct()
        print(sido)
        sido_list = EntrcSidoFirstSerializer(sido, many=True)  # 시- 도 return
        # print(sido_list)
        return Response(sido_list.data, status=200)


class GetReSigunguViewSet(APIView):
    """
    POST /getSigungu
    """

    def post(self, request, **kwargs):
        sel_sido_cd = request.data['sido_cd']

        sigungu = EntrcSido.objects.values('sigungu_nm').annotate(
            sigungu_cd=(Substr('doro_cd', 3, 3))).distinct().filter(sido_cd=sel_sido_cd)
        print(sigungu)
        sigungu_list = EntrcSidoSecondSerializer(sigungu, many=True)  # 시- 도 return
        # print(sigungu_list)
        return Response(sigungu_list.data, status=200)


class GetReDongViewSet(APIView):
    """
    POST /getDong
    """

    def post(self, request, **kwargs):
        sel_sido_cd = request.data['sido_cd']
        sel_sigungu_cd = request.data['sigungu_cd']

        dong = EntrcSido.objects.values('dong_nm', 'dong_cd').distinct().filter(sido_cd=sel_sido_cd,
                                                                                sigungu_cd=sel_sigungu_cd).exclude(
            dong_nm__exact='')

        print(dong)
        dong_list = EntrcSidoThirdSerializer(dong, many=True)  # 시- 도 return

        return Response(dong_list.data, status=200)


# # RetrieveAPIView 하나만 불러오는 거
class PostDetailViewSet(RetrieveAPIView):
    lookup_field = 'b_id'
    queryset = Posts.objects.all()
    serializer_class = PostDetailSerializer


class PostDetailUpdateViewSet(APIView):
    """
    POST /board/updateviews
    """

    def post(self, request, **kwargs):
        res_data = {
            "success": True,
            "error": None
        }

        b_id = request.data['b_id']
        now_post = Posts.objects.get(b_id=b_id)

        if now_post.b_views == '':
            now_post.b_views = 1
        else:
            now_post.b_views = str(int(now_post.b_views) + 1)

        now_post.save()

        return Response(res_data, status=200)


class PostCommentDetailViewSet(APIView):
    def delete(self, request, pc_id):
        res_data = {
            "success": True,
            "error": None
        }

        try:    
            postcommentObj = PostComment.objects.get(pc_id=pc_id)
            postcommentObj.delete()

            return Response(res_data, status=200)
        except Exception as e: 
            res_data['error'] = e
            
            return Response(res_data, status=200)


class PostUpdateViewSet(UpdateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostDetailSerializer


class PostDeleteViewSet(DestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostDetailSerializer

