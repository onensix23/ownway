import json, requests

from allauth.socialaccount.providers.oauth2.client import OAuth2Client
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
from rest_framework.authtoken.models import Token
from snsP.storages import FileUpload, s3_client

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from .serializers import *
from .models import *
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
            res_data['error'] = e

        # print(res_data)
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
        if request_d['socialType'] == 'login':
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

            res_data = {
                'exist_user' : True,
            }

            # 유저가 새로 생성되었다면
            if user_created:
                user.first_name = facebook_name
                user.email = facebook_email
                user.save()

                UserProfile.objects.create(up_id=user)
                res_data['exist_user']=False

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return Response(res_data, status=200)


class FollowUserViewSet(APIView):
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
        
        print(user_id)
        print(page_host_id)

        readerObj = User.objects.get(username=page_host_id) # 따라오게 하는 사람
        readingObj = User.objects.get(username=user_id) # 따라가는 사람

        if request.data['type'] == '0': # 체크용
            query_count = UserFollow.objects.filter(uf_reader=page_host_id, uf_reading=user_id).count()

            if query_count == 0:
                res_data['count'] = query_count
                res_data["is_following"] = False
            else:
                res_data["count"] = 0
        else:
            userFollowObj, isCreated =  UserFollow.objects.get_or_create(uf_reader=readerObj, uf_reading=readingObj)

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


class UserViewSet(APIView):
    """
        POST /login/
        description
            - 로그인
        param
            - userId
            - uesrPassword
    """

    @method_decorator(csrf_exempt)
    def post(self, request, **kwargs):
        request_d = request.data  # {"userId":"rohhj622","userPassword":"shgsuwls1!"}

        response_data = {
            'success': False,
            'error': None

        }

        login_username = request_d['userId']
        login_password = request_d['userPassword']

        # print(login_username, login_password)

        if not (login_username and login_password):
            response_data['error'] = "아이디와 비밀번호를 모두 입력해주세요."
        else:
            myuser = User.objects.get(username=login_username)

            if myuser.check_password(login_password):
                print("비번 맞아")
            else:
                print("틀리다고?")

            myuser = authenticate(username=login_username, password=login_password)
            # db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.
            # print(myuser)
            if myuser is not None:
                login(request, myuser)
                # request.session['user'] = myuser.username
                #     # 세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                #     # 세션 user라는 key에 방금 로그인한 id를 저장한것.
                response_data['success'] = True
            else:
                response_data['error'] = "비밀번호를 틀렸습니다."

        return Response(response_data, status=200)
    

# ResigterUserViewSet
class ResigterUserViewSet(APIView):
    """
        POST /register/
        description
            - 회원가입
        param
            - id1, password, nickname, email, re_password
            - uesrPassword
    """
    def post(self, request, **kwargs):
        request_d = request.data  # {"userId":"rohhj622","userPassword":"shgsuwls1!"}

        response_data = {
            'success': False,
            'error': None
        }

        # id1 = request_d['id1']  # 딕셔너리형태
        # password = request_d['password']
        # nickname = request_d['nickname']
        # email = request_d['email']
        # re_password = request_d['re_password']
        #
        # res_data = {
        #     'success': False,
        # }
        #
        # if not (id1 and password and re_password and email and nickname):
        #     res_data['error1'] = "모든 값을 입력해야 합니다."
        # elif password != re_password:
        #     # return HttpResponse('비밀번호가 다릅니다.')
        #     res_data['error2'] = '비밀번호가 다릅니다.'
        # elif (User.objects.filter(username=id1)).count() != 0:
        #     res_data['error3'] = '중복된 ID 입니다.'
        # else:
        #     # username id ,
        #     #m_password = make_password(password, None, 'pbkdf2_sha256')
        #     #user = User.objects.create_user(username=id1, password=m_password,first_name=nickname, email=email)
        #     res_data['success'] = "가입되었습니다."

        id1 = request_d['id1']  # 딕셔너리형태
        password = request_d['password']
        nickname = request_d['nickname']
        email = request_d['email']

        # print("password:"+password);

        res_data = {
            'success': False,
        }

        if not (id1 and password and email and nickname):
            res_data['error'] = "모든 값을 입력해야 합니다."
        elif (User.objects.filter(username=id1)).count() != 0:
            res_data['error'] = '중복된 ID 입니다.'
        else:
            # username id ,
            m_password = make_password(password, None, 'pbkdf2_sha256')
            User.objects.create_user(username=id1, password=m_password, first_name=nickname, email=email)
            res_data['success'] = "가입되었습니다."

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
        }

        logout(request)
        # response.delete_cookie('user_location')
        res_data['success'] = True
        return Response(res_data, status=200)


