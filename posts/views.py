from django.db.models.functions import Substr
from django.shortcuts import render, redirect
from snsP.my_settings import *
from django.http import HttpResponse
from django.db.models import Q,Subquery,Prefetch,F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from snsP.storages import FileUpload, s3_client
from .serializers import *
from .models import *
from users.models import UserFollow, UserBlock, UserNotiCount
from notis.views import *
import threading, requests, asyncio
import subprocess

class TestViewSet(APIView):
    def get(self, request, **kwargs):
        res_data = {
            "success": True,
            "error": None,
            "fileName": '',
            "image_cnt":0
        }
        url = 'http://172.30.1.44:8001/api/alert_noti'

        params =  {
            'fields': ','.join([
                'id',
                'name',
                'email',
                # 'first_name',
                # 'last_name',
                # 'picture',
            ]),
        }
        response = requests.post(url, params)

        return Response('done', status=200)


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
        postObj.b_update_datetime = datetime.now()
        postObj.save()

        cnt = 0
        zero_cnt = 0

        if request.FILES:
            for k in request.FILES.keys():
                if k.find('uploadFile') != -1:
                    cnt = cnt + 1
                    # print(request.FILES[k])

                    photo = Photo()
                    photo.b_id = postObj

                    if request.data['type'] != 1:
                        photo.p_filename = FileUpload(s3_client).upload(request.FILES[k])
                    else: # THUMBNAIL
                        photo.p_filename = FileUpload(s3_client).uploadthumbnail(request.FILES[k])
                        
                    photo.p_isthumb = request.data['type']

                    # 데이터베이스에 저장
                    photo.save()

                    res_data[k] = request.FILES[k].name
                    
                    if photo.p_isthumb == '0':
                        zero_cnt = zero_cnt + 1
                    
        if zero_cnt != 0:
            # -, -, b_id, id, type, -, -
            UserNotiCount.objects.filter(unc_b_id=postObj).update(unc_count=F('unc_count')+1) #다 하나씩 올리고 그 다음엔?
            UserNotiCount.objects.filter(unc_b_id=postObj,unc_count=4).delete() #지울거 지우기

            param1 = "python3 ./lambda_function.py " 
            param1 = param1 + "'true'" + " "
            param1 = param1 + "'true'" + " '"
            param1 = param1 + request.data['b_id'] + "' '"
            param1 = param1 + str(postObj.id) + "' "
            param1 = param1 + "'im_c'" + " "
            param1 = param1 + "'true'"

            process = subprocess.Popen(param1, shell=True)
                    
        res_data['image_cnt'] = cnt
        
        return Response(res_data, status=200)

    def put(self, request, **kwargs):
        res_data = {
            "success": True,
            "error": None,
            "fileName": '',
            "image_cnt":0
        }
        cnt = 0
        if request.FILES:
            for k in request.FILES.keys():
                if k.find('uploadFile') != -1:
                    cnt = cnt + 1 

                    photoObj = Photo.objects.get(b_id=request.data['b_id'], p_isthumb='1')
                    exFile = photoObj.p_filename
                    photoObj.p_filename = FileUpload(s3_client).upload(request.FILES[k])

                    # 데이터베이스에 저장
                    photoObj.save()

                    FileUpload(s3_client).delete(exFile)

                    res_data[k] = request.FILES[k].name
                    
                    # t = threading.Thread(target=send_to_user_about_who_add_image('im_c', True, userObj, postObj))
                    # t.start()
                    
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
        
        # print(request.data)

        photoObj = Photo.objects.get(b_id=b_id,p_id=p_id)

        try: 
            if p_filename != None:
                FileUpload(s3_client).delete(p_filename)
            
            photoObj.delete()
        except Exception as e:
            print('except')
            print(e)
            # return Response(res_data, status=200)
        
        return Response(res_data, status=200)



class PostViewSet(APIView):

    """
       POST /board
    """
    def post(self, request, **kwargs):

        res_data = {
            'post_success': False,
            'postcomment_success': 'no comment',
            'b_id': 6
        }


        user_id = request.data['user_id']
        userObj = User.objects.get(username=user_id)

        if request.data['type'] == 'create':
            b_title = request.data['b_title']
            b_address = request.data['b_address']
            b_theme = request.data['b_theme']
            b_hash_tag_1 = request.data['b_hash_tag_1']
            b_hash_tag_2 = request.data['b_hash_tag_2']
            b_place_id = request.data['b_place_id']

            pc_comment = request.data['pc_comment']

            # print(request.data)


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

        elif request.data['type'] == 'read':
            get_queryset = Posts.objects.prefetch_related('photo_b_id').prefetch_related('postcomment_b_id').prefetch_related('savepost_b_id').select_related('id').order_by('-b_update_datetime').filter(Q(
                ~Q(id__in=User.objects.filter(username__in=Subquery(UserBlock.objects.values('ub_to').filter(ub_from=userObj))))
            ))

            get_serializer_class = PostSerializer(get_queryset, many=True)
            res_data = get_serializer_class.data

        elif request.data['type'] == 'readDetail':
            get_queryset = Posts.objects.prefetch_related('photo_b_id').prefetch_related(
                Prefetch('postcomment_b_id',
                queryset=PostComment.objects.filter(~Q(id__in=User.objects.filter(username__in=Subquery(UserBlock.objects.values('ub_to').filter(ub_from=userObj)))))
                )).prefetch_related('postplace_b_id').prefetch_related('savepost_b_id').filter(Q(
                Q(b_id=request.data['b_id']) 
            )).select_related('id') # .order_by('-photo_b_id.p_datetime').order_by('-postplace_b_id.pp_datetime').order_by('-postcomment_b_id.pc_datetime')
            get_serializer_class = PostSerializer(get_queryset, many=True)
            res_data = get_serializer_class.data

        return Response(res_data, status=200)

    """
    GET /board
        detail (b_id)
    """
    def get(self, request, **kwargs):
        if(len(request.GET) > 0): #detail
            get_queryset = Posts.objects.prefetch_related('photo_b_id').prefetch_related('postcomment_b_id').prefetch_related('postplace_b_id').prefetch_related('savepost_b_id').filter(Q(
                Q(b_id=request.GET['b_id']) 
            )).select_related('id') # .order_by('-photo_b_id.p_datetime').order_by('-postplace_b_id.pp_datetime').order_by('-postcomment_b_id.pc_datetime')
            get_serializer_class = PostSerializer(get_queryset, many=True)

        else:
            get_queryset = Posts.objects.prefetch_related('photo_b_id').prefetch_related('postcomment_b_id').prefetch_related('savepost_b_id').select_related('id').order_by('-b_update_datetime')
            get_serializer_class = PostSerializer(get_queryset, many=True)

        # return Response(get_serializer_class2.data, status=200)
        return Response(get_serializer_class.data, status=200)

    """
        PUT /board/{b_id}
    """
    def put(self, request, **kwargs):
        res_data = {
            "success": True,
            "error": None
        }

        b_id = request.data['b_id']

        postObj= Posts.objects.get(b_id=b_id)

        postObj.b_title = request.data['b_title']
        postObj.b_address = request.data['b_address']
        postObj.b_theme = request.data['b_theme']
        postObj.b_hash_tag_1 = request.data['b_hash_tag_1']
        postObj.b_hash_tag_2 = request.data['b_hash_tag_2']

        postObj.save()

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

            # print(get_queryset)
            # print(get_queryset.values_list())

            lp_id_list = []

            for vl in get_queryset.values_list():
                lp_id_list.append(vl[2])

            res_queryset = Posts.objects.filter(b_id__in=lp_id_list)

            get_serializer_class = PostDetailSerializer(res_queryset, many=True)
            # print(get_serializer_class.data)
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

        type = request.data['type']

        # noti_receiver = UserFCMToken.objects.get(ufcm_user_id=User.objects.get(username=postObj.id).username, ufcm_device_id=ufcm_device_id) # 글 작성자

        if type == 'c' :
            # select
            user_id = request.data['userId']
            b_id = request.data['b_id']
            pc_comment = request.data['pc_comment']

            userObj = User.objects.get(username=user_id)
            postObj = Posts.objects.get(b_id=b_id)
            
            new_Comment = PostComment(id=userObj, b_id=postObj, pc_comment=pc_comment)
            new_Comment.save()  # insert
                
            # 내가 내 글에 글 씀 -> 구독자한테 알림 가야됨
            if str(postObj.id) == str(user_id):
                UserNotiCount.objects.filter(unc_b_id=postObj).update(unc_count=F('unc_count')+1) #다 하나씩 올리고 그 다음엔?
                UserNotiCount.objects.filter(unc_b_id=postObj,unc_count=4).delete() #지울거 지우기

                # pc_id, pc_comment, pc_type, b_id, id, type, who's comment
                param1 = "python3 ./lambda_function.py " 
                param1 = param1 + str(new_Comment.pc_id) + " "
                param1 = param1 +"'"+ pc_comment +"' "
                param1 = param1 + str(b_id) + " "
                param1 = param1 + user_id + " "
                param1 = param1 + "'pc_c'" + " "
                param1 = param1 + "'true'"

                process = subprocess.Popen(param1, shell=True)

                postObj.b_update_datetime = datetime.now()
                postObj.save()

            else: # 내 글은 아닌데 누군가의 글에 답글이 달린 상태겠죠?
                new_noticount, is_created = UserNotiCount.objects.get_or_create(unc_user_id=userObj, unc_b_id=postObj)

                # 기존에 있다면
                if is_created == False:
                    new_noticount.unc_count = 0
                    new_noticount.save()
                    
                # pc_id, pc_comment, pc_type, b_id, id, type, who's comment
                param1 = "python3 ./lambda_function.py " 
                param1 = param1 + str(new_Comment.pc_id) + " "
                param1 = param1 +"'"+ pc_comment +"' "
                param1 = param1 + "'0'"
                param1 = param1 + str(b_id) + " "
                param1 = param1 + user_id + " "
                param1 = param1 + "'pc_c'" + " "
                param1 = param1 + "'false'"

                process = subprocess.Popen(param1, shell=True)

        elif type == 'u':
            pc_id = request.data['pc_id']
            pcObj = PostComment.objects.get(pc_id=pc_id)

            pcObj.pc_comment = pc_comment
            pcObj.save()

        elif type == 'd':
            try:    
                user_id  = request.data['user_id']
                b_id = request.data['b_id']
                pc_id = request.data['pc_id']

                postObj = Posts.objects.get(b_id=b_id)
                userObj = User.objects.get(username=user_id)


                if str(postObj.id) != str(user_id):
                    pcCount = PostComment.objects.filter(id=userObj, b_id=postObj).count()
                    if pcCount == 1:
                        uncObj = UserNotiCount.objects.get(unc_b_id=postObj,unc_user_id=userObj)
                        uncObj.delete()
                
                postcommentObj = PostComment.objects.get(pc_id=pc_id)
                postcommentObj.delete()

            except Exception as e:
                res_data['error'] = e

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

            if str(user_id) == str(postId.id):
                UserNotiCount.objects.filter(unc_b_id=postId).update(unc_count=F('unc_count')+1) #다 하나씩 올리고 그 다음엔?
                UserNotiCount.objects.filter(unc_b_id=postId,unc_count=4).delete() #지울거 지우기

                # pc_id, pc_comment, pc_type, b_id, id, type, who's comment
                param1 = "python3 ./lambda_function.py " 
                param1 = param1 + "'true'" + " "
                param1 = param1 + "'true'" + " "
                param1 = param1 + str(b_id) + " "
                param1 = param1 + user_id + " "
                param1 = param1 + "'pp_c'" + " "
                param1 = param1 + "'true'"

                process = subprocess.Popen(param1, shell=True)
                    
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
        get_queryset = Posts.objects.filter(id__in=Subquery(UserFollow.objects.values('uf_reader').filter(uf_reading=user_id)), b_del='N').order_by('-b_update_datetime')
        # print(Posts.objects.filter(id__in=Subquery(UserFollow.objects.values('uf_reader').filter(uf_reading=user_id)), b_del='N').order_by('-b_datetime'))
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

        get_queryset = Posts.objects.filter(b_id__in=Subquery(SavePost.objects.values('b_id').filter(id=user_id))).prefetch_related('photo_b_id').prefetch_related('savepost_b_id').select_related('id').order_by('-b_update_datetime')
        get_serializer_class = PostSerializer(get_queryset, many=True)

        return Response(get_serializer_class.data, status=200)


    def post(self, request, **kwargs):
        res_data = {
            'action' : 'create',
            'count' : 0,
            "success" : True,
            'data' : None
        }

        user_id = request.data['userId']
        b_id = request.data['b_id']

        userObj = User.objects.get(username=user_id)
        postObj = Posts.objects.get(b_id=b_id)

        if request.data['type'] == '0':
            query = SavePost.objects.filter(id=user_id, b_id=b_id)

            if query.count() > 0:
                res_data['count'] = query.count()
                res_data['data'] = SavePost.objects.get(id=user_id, b_id=b_id).sp_is_noti
            
        else:
            savePostObj, isCreated =  SavePost.objects.get_or_create(id=userObj, b_id=postObj)
            
            if isCreated == False: # 삭제 해야 됨
                res_data['action'] = 'delete'
                savePostObj.delete()
            elif isCreated == True:
                if str(user_id) != str(postObj.id):
                    # 내가 아닌 누군가가 글 구독!

                    # pc_id, pc_comment, pc_type, b_id, id, type, who's comment
                    param1 = "python3 ./lambda_function.py " 
                    param1 = param1 + "'true'" + " "
                    param1 = param1 + "'true'" + " "
                    param1 = param1 + str(postObj.id) + " "
                    param1 = param1 + user_id + " "
                    param1 = param1 + "'sp_c'" + " "
                    param1 = param1 + "'true'"

                    process = subprocess.Popen(param1, shell=True)

        return Response(res_data, status=200)

    def put(self, request, **kwargs):
        res_data = {
            'action' : None,
            'result' : True,
            "success" : True,
            'error' : None
        }

        user_id = request.data['userId']
        b_id = request.data['b_id']

        userObj = User.objects.get(username=user_id)
        postObj = Posts.objects.get(b_id=b_id)

        savePostObj = SavePost.objects.get(id=userObj, b_id=postObj)

        try:
            if savePostObj.sp_is_noti == True:
                savePostObj.sp_is_noti = False
                res_data['action'] = False
                savePostObj.save()

            elif savePostObj.sp_is_noti == False:
                savePostObj.sp_is_noti = True
                res_data['action'] = True
                savePostObj.save()

        except Exception as e:
            res_data['error'] = e
            
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


# RetrieveAPIView 하나만 불러오는 거
class PostDetailViewSet(APIView):
    """
        DELETE /board/{b_id}
    """
    def delete(self, request, b_id):
        res_data = {
            "success": True,
            "error": None
        }

        try:    
            photoObj = Photo.objects.filter(b_id=b_id)
            k = PhotoSerializer(photoObj, many=True)

            for odict in k.data:
                for key, value in odict.items():
                    if key == 'p_filename':
                        FileUpload(s3_client).delete(value)
                        # print(value)

            queryset = Posts.objects.get(b_id=b_id)
            queryset.delete()

        except Exception as e: 
            res_data['error'] = e
        
        return Response(res_data, status=200)


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


class PostUpdateViewSet(UpdateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostDetailSerializer


class PostDeleteViewSet(DestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostDetailSerializer

