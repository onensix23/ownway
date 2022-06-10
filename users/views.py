import json, requests, subprocess
import threading

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# 비밀번호 암호화 / 패스워드 체크(db에있는거와 일치성확인)
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_auth.registration.serializers import SocialLoginSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from snsP.storages import FileUpload, s3_client

from .serializers import *
from .models import *
from notis.views import *
from posts.models import Posts, Photo
from posts.serializers import PostSerializer

class ResignUserViewSet(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, **kwargs):
        res_data = {
            "action" : "delete user",
            "success" : True,
            'error': '',
        }
        user_id = request.data['id']
        print('user_id')
        print(user_id)

        userObj = User.objects.get(username=user_id)
        
        userProfileObj = UserProfile.objects.get(up_id=user_id)

        try:
            postObj = Posts.objects.filter(id=user_id)
            k = PostSerializer(postObj, many=True)

            for odict in k.data:
                for key, value in odict.items():
                    if key == 'photo_b_id':
                        if len(value) > 0 :
                            for modict in value:
                                for p_key, p_val in modict.items():
                                    print(p_key)
                                    if p_key == 'p_filename':
                                        if p_val != None and p_val.find('https://') != -1:
                                            FileUpload(s3_client).delete(p_val)
                                        break
                            break

            if userProfileObj.up_imagename != None :
                FileUpload(s3_client).delete(userProfileObj.up_imagename)

            userObj.delete()

        except Exception as e: 
            print('e')
            print(e)
            res_data['error'] = e

        print(res_data)
        return Response(res_data, status=200)

class UserDataViewSet(APIView):

    @method_decorator(csrf_exempt)
    def post(self, request, **kwargs):
        print(request.data)

        res_data = {
            "action" : "save data",
            "count" : 0,
            'image_cnt': 0,
            "success" : True
        }

        user_id = request.data['id']
        userObj = User.objects.get(username=user_id)

        if request.data['firstname']:
            userObj.first_name = request.data['firstname']
            userObj.save()

            res_data['count'] = res_data['count'] + 1


        userProfileObj = UserProfile.objects.get(up_id=user_id)

        cnt = 0

        if request.FILES:
            for k in request.FILES.keys():
                if k.find('uploadFile') != -1:
                    # print(userProfileObj.up_imagename)
                    if userProfileObj.up_imagename != None:
                        FileUpload(s3_client).delete(userProfileObj.up_imagename)

                    cnt = cnt + 1
                    
                    userProfileObj.up_imagename = FileUpload(s3_client).upload(request.FILES[k])

                    # 데이터베이스에 저장
                    userProfileObj.save()

                    res_data[k] = request.FILES[k].name
                    
        res_data['image_cnt'] = cnt

        return Response(res_data, status=200)

class SocialLoginViewSet(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, **kwargs):
        request_d = request.data  # {"userId":"rohhj622","userPassword":"shgsuwls1!"}
        res_data = {
            'exist_user' : True,
        }

        if request_d['socialType'] == 'facebook':
            if request_d['type'] == 'login':
                url = 'https://graph.facebook.com/v3.0/me'
                params =  {
                    'fields': ','.join([
                        'id',
                        'name',
                        'email',
                        # 'first_name',
                        # 'last_name',
                        # 'picture',
                    ]),
                    # 'fields': 'id,name,first_name,last_name,picture',
                    'access_token': request_d['data']['accessToken']
                }
                response = requests.get(url, params)
                response_dict = response.json()
                # print(response_dict)

                facebook_user_id = response_dict['id']
                facebook_name = response_dict['name']

                if 'email' in response_dict.keys():
                    facebook_email = response_dict['email']
                else:
                    facebook_email = ''

                user, user_created = User.objects.get_or_create(username=facebook_user_id)

                # 유저가 새로 생성되었다면
                if user_created:
                    user.first_name = facebook_name
                    user.email = facebook_email
                    user.save()

                    UserProfile.objects.create(up_id=user)
                    res_data['exist_user']=False

                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            if request_d['type'] == 'login':
                google_user_id = request_d['data']['user']['id']
                google_name = request_d['data']['user']['name']

                if 'email' in request_d['data']['user'].keys():
                    google_email = request_d['data']['user']['email']
                else:
                    google_email = ''

                user, user_created = User.objects.get_or_create(username=google_user_id)

                # 유저가 새로 생성되었다면
                if user_created:
                    user.first_name = google_name
                    user.email = google_email
                    user.save()

                    UserProfile.objects.create(up_id=user)
                    res_data['exist_user']=False

                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return Response(res_data, status=200)

class FollowUserViewSet(APIView):

    def get(self, request, **kwargs):
        user_id = request.GET.get('user_id')
        type = request.GET.get('type')

        if type == 'reading':
            temp = UserFollow.objects.filter(uf_reading=user_id).values('uf_reader')
            readingObj = User.objects.filter(username__in=temp) # 따라가는 사람
            serialize_data = UserSerializer3(readingObj, many=True)

        elif type == 'reader':
            temp = UserFollow.objects.filter(uf_reader=user_id).values('uf_reading')
            readerObj = User.objects.filter(username__in=temp) #따라오게 하는 사람
            serialize_data = UserSerializer3(readerObj, many=True)

        return Response(serialize_data.data, status=200)

    @method_decorator(csrf_exempt)
    def post(self, request, **kwargs):

        res_data = {
            "action" : "create",
            "count" : 0,
            "is_following" : True,
            "success" : True
        }

        user_id = request.data['userId']
        page_host_id = request.data['myPageHost']
        
        readerObj = User.objects.get(username=page_host_id) # 따라오게 하는 사람 following
        readingObj = User.objects.get(username=user_id) # 따라가는 사람 follower

        if request.data['type'] == '0': # 체크용
            query_count = UserFollow.objects.filter(uf_reader=page_host_id, uf_reading=user_id).count()

            if query_count == 0:
                res_data['count'] = query_count
                res_data["is_following"] = False
            else:
                res_data["count"] = 0
        elif request.data['type'] == '1':
            userFollowObj, isCreated =  UserFollow.objects.get_or_create(uf_reader=readerObj, uf_reading=readingObj)

            if isCreated == False: # 삭제 해야 됨
                res_data['action'] = 'delete'
                userFollowObj.delete()
            elif isCreated == True: 
                # 내가 아닌 누군가가 글 구독!
                param1 = "python3 ./lambda_function.py " 
                param1 = param1 + "'true'" + " "
                param1 = param1 + "'true'" + " "
                param1 = param1 + str(readerObj.username) + " "
                param1 = param1 + str(readingObj.username) + " "
                param1 = param1 + "'fu_c'" + " "
                param1 = param1 + "'true'"

                process = subprocess.Popen(param1, shell=True)
                
        elif request.data['type'] == '2': # 리더 삭제 시 불려짐
            userFollowObj, isCreated =  UserFollow.objects.get_or_create(uf_reader=readingObj, uf_reading=readerObj)

            if isCreated == False: # 삭제 해야 됨
                res_data['action'] = 'delete'
                userFollowObj.delete()

        return Response(res_data, status=200)

class BlockUserViewSet(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, **kwargs):
        res_data = {
            "action" : "block",
            "error" : None,
            'is_already_block':True,
            "success" : True
        }

        from_id = request.data['from_id'] # 차단 누른 사람
        fromObj = User.objects.get(username=from_id) # 차단 누른 사람

        if request.data['type'] == '0': # 체크용

            to_id = request.data['to_id'] # 차단 당하는 사람
            toObj = User.objects.get(username=to_id) # 차단 당하는 사람
            
            query_count = UserBlock.objects.filter(ub_from=fromObj, ub_to=toObj).count()
            try:
                if query_count == 0:
                    res_data['count'] = query_count
                    res_data["is_already_block"] = False
                else:
                    res_data["count"] = 0
            except Exception as e:
                res_data['success'] = False
                res_data['error'] = e

        elif request.data['type'] == '1': # 실제로 동작
            to_id = request.data['to_id'] # 차단 당하는 사람
            toObj = User.objects.get(username=to_id) # 차단 당하는 사람

            userBlockObj, isCreated =  UserBlock.objects.get_or_create(ub_from=fromObj, ub_to=toObj)

            try:
                if isCreated == False: # 삭제 해야 됨
                    res_data['action'] = 'unblock'
                    res_data["is_already_block"] = False
                    userBlockObj.delete()

                elif isCreated == True: 
                    # 차단함...
                    # 내가 그 사람한테 단 댓글 삭제
                    # 팔로우 삭제 0
                    # 구독한 거 있으면 삭제 
                    userFollowObj_to = UserFollow.objects.filter(uf_reader=fromObj, uf_reading=toObj)
                    if userFollowObj_to != None:
                        userFollowObj_to.delete()

                    userFollowObj_from = UserFollow.objects.filter(uf_reader=toObj, uf_reading=fromObj)
                    if userFollowObj_from != None:
                        userFollowObj_from.delete()

                    savePostObj_from = SavePost.objects.filter(b_id__in=Subquery(Posts.objects.values('b_id').filter(id=toObj)), id=fromObj)
                    if savePostObj_from != None:
                        savePostObj_from.delete()
                    
                    savePostObj_to = SavePost.objects.filter(b_id__in=Subquery(Posts.objects.values('b_id').filter(id=fromObj)), id=toObj)
                    if savePostObj_to != None:
                        savePostObj_to.delete()

                    postcommentObj_from= PostComment.objects.filter(b_id__in=Subquery(Posts.objects.values('b_id').filter(id=fromObj)), id=toObj)
                    if postcommentObj_from != None:  
                        postcommentObj_from.delete()

                    postcommentObj_to= PostComment.objects.filter(b_id__in=Subquery(Posts.objects.values('b_id').filter(id=toObj)), id=fromObj)
                    if postcommentObj_to != None:  
                        postcommentObj_to.delete()
            except Exception as e:
                res_data['success'] = False
                res_data['error'] = e
        elif request.data['type'] == '2': # 차단한 사람 내용 불러오기
            get_queryset = UserBlock.objects.filter(ub_from=fromObj)
            get_serializer_class = UserBlockSerializer(get_queryset, many=True)
            res_data = get_serializer_class.data
            
        return Response(res_data, status=200)

class UserProfileViewSet(APIView):

    @method_decorator(csrf_exempt)
    def post(self, request, **kwargs):
        
        request_d = request.data; #{"user_id":"1088384478597823"}
        user_id = request_d['userId']
        userObj = User.objects.get(username=user_id)

        userProfile, user_created = UserProfile.objects.get_or_create(up_id=userObj)

        get_queryset = UserProfile.objects.get(up_id=user_id)
        get_serializer_class = UserProfileSerializer(get_queryset, many=False)

        get_query_user_reader = UserFollow.objects.filter(uf_reader=user_id).count()
        get_query_user_reading = UserFollow.objects.filter(uf_reading=user_id).count()
        get_query_user_message = Posts.objects.filter(id=user_id).count()

        response_data = {
            'result' : get_serializer_class.data,
            'reader' : get_query_user_reader,
            'reading' : get_query_user_reading,
            'message' : get_query_user_message
        }

        # print(response_data)

        return Response(response_data, status=200)


class UserNotificationSet(APIView):
    def get(self, request, **kwargs):
        res_data = {
            'success': False,
            'error': None,
            'result' : '',
            
        }

        userId = request.GET.get('userId')
        deviceId = request.GET.get('deviceId')
        token = request.GET.get('tokenId')

        userObj = User.objects.get(username=userId)
        userFCMObj = UserFCMToken.objects.get(ufcm_user_id=userObj,ufcm_device_id=deviceId,ufcm_token=token)

        userNotificationObj = UserNotification.objects.filter(un_token_id=userFCMObj, un_to=userObj, un_is_sended=True, un_is_read=False).count()
        res_data['result'] = userNotificationObj
        
        return Response(res_data, status=200)

    def post(self, request, **kwargs):
        res_data = {
            'success': False,
            'error': None,
            'action' : '',
        }

        user_id = request.data['userId']
        device_id = request.data['deviceId']
        token = request.data['token']

        userObj = User.objects.get(username=user_id)
        userFCMObj = UserFCMToken.objects.get(ufcm_user_id=userObj,ufcm_device_id= device_id,ufcm_token=token)

        try:
            userNotificationObj = UserNotification.objects.filter(un_token_id=userFCMObj,un_to=userObj, un_is_sended=True, un_is_read=False).order_by("-un_send_date")
            get_serializer_class = UserNotificationSerializer2(userNotificationObj, many=True)         
            res_data['success'] = True

            return Response(get_serializer_class.data, status=200)

        except Exception as e:
            res_data['error'] = e

            return Response(res_data, status=200)

    def put(self, request, **kwargs):
        res_data = {
            'success': False,
            'error': None,
            'action' : '',
        }

        if request.data['type'] == 'delete':
            try:
                user_id = request.data['userId']

                userObj = User.objects.get(username=user_id)
                UserNotification.objects.filter(un_to=userObj).update(un_is_read=True)
                # userNotificationObj.un_is_read = True
                # userNotificationObj.save()

                res_data['success'] = True
            
            except Exception as e:
                res_data['error'] = e

        elif request.data['type'] == 'update':
            try: 
                un_id = request.data['un_id']

                userNotificationObj = UserNotification.objects.get(un_id=un_id)
                userNotificationObj.un_is_read = True
                userNotificationObj.save()

                res_data['success'] = True

            except Exception as e:
                res_data['error'] = e

        elif request.data['type'] == 'updateall':
            try: 
                # {'user_id': '101960524939177545327', 'b_id': 114, 'type': 'updateall'}

                user_id = request.data['user_id']
                b_id = request.data['b_id']

                # print(request.data)
                toObj = User.objects.get(username=user_id)
                postObj = Posts.objects.get(b_id=b_id)

                userNotificationObj = UserNotification.objects.filter(un_to=toObj, un_etc=postObj).update(un_is_read=True)

                res_data['success'] = True

            except Exception as e:
                res_data['error'] = e

        return Response(res_data, status=200) 



class UserFCMTokenViewSet(APIView):

    def post(self, request, **kwargs):
        request_d = request.data

        ufcm_user_id = request_d['userId']
        ufcm_token = request_d['fcmToken']
        ufcm_device_id = request_d['deviceId']

        userObj = User.objects.get(username=ufcm_user_id)

        res_data = {
            'success': False,
            'error': None,
            'action' : '',
        }

        try:
            userFCMTokenObj, isCreated = UserFCMToken.objects.get_or_create(ufcm_user_id=userObj, ufcm_device_id=ufcm_device_id)

            if isCreated:
                userFCMTokenObj.ufcm_token = ufcm_token
                userFCMTokenObj.save()

                res_data['action'] = 'first create token'

            else:
                if str(userFCMTokenObj.ufcm_token) != str(ufcm_token):

                    userFCMTokenObj.ufcm_token = ufcm_token

                    userFCMTokenObj.ufcm_token_add = datetime.now()
                    userFCMTokenObj.ufcm_token_check = datetime.now()

                    userFCMTokenObj.save()

                    res_data['action'] = 'token refresh'

                else:
                    userFCMTokenObj.ufcm_token_check = datetime.now()
                    res_data['action'] = 'noting'

            res_data['success'] = True

        except Exception as e:
            res_data['error'] = e
            
        return Response(res_data, status=200)


#Login
class LogoutUserViewSet(APIView):
    """
        Post /logout/
        description
            - 로그아웃
    """
    @method_decorator(csrf_exempt)
    def post(self, request):

        res_data = {
            'success': False,
            'error': None,
        }

        try:
            userObj = User.objects.get(username=request.data['userId'])
            userFCMObj = UserFCMToken.objects.get(ufcm_user_id=userObj, ufcm_device_id=request.data['deviceId'])
            
            userFCMObj.ufcm_token = None
            
            userFCMObj.save()

            logout(request)

            res_data['success'] = True

        except Exception as e:
            print(e)
            res_data['error'] = e

        return Response(res_data, status=200)


