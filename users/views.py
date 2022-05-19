import json, requests
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
                                        print("2")
                                        if p_val != None and p_val.find('https://') != -1:
                                            print("3")
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
                t = threading.Thread(target=send_to_user_about_who_followed_user('fu_c', readingObj, readerObj))# , noti_receiver.ufcm_token, noti_receiver.ufcm_device_id))
                t.start()
                
        elif request.data['type'] == '2': # 리더 삭제 시 불려짐
            userFollowObj, isCreated =  UserFollow.objects.get_or_create(uf_reader=readingObj, uf_reading=readerObj)

            if isCreated == False: # 삭제 해야 됨
                res_data['action'] = 'delete'
                userFollowObj.delete()

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
    def post(self, request, **kwargs):

        res_data = {
            'success': False,
            'error': None,
            'action' : '',
        }

        user_id = request.data['userId']
        userObj = User.objects.get(username=user_id)

        try:
            userNotificationObj = UserNotification.objects.filter(un_to=userObj).order_by("-un_send_date")
            get_serializer_class = UserNotificationSerializer(userNotificationObj, many=True)         
            res_data['success'] = True


            return Response(get_serializer_class.data, status=200)

        except Exception as e:
            res_data['error'] = e
            return Response(res_data, status=200)
            
        # return Response(res_data, status=200)


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


