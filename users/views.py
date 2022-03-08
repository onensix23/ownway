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

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from .serializers import *
from .models import UserProfile

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
                    'first_name',
                    'last_name',
                    'picture',
                ]),
                # 'fields': 'id,name,first_name,last_name,picture',
                'access_token': request_d['data']['accessToken']
            }
            response = requests.get(url, params)
            response_dict = response.json()

            facebook_user_id = response_dict['id']
            facebook_name = response_dict['name']
            facebook_email = response_dict['email']

            user, user_created = User.objects.get_or_create(username=facebook_user_id)

            # 유저가 새로 생성되었다면
            if user_created:
                # print(user_created)

                user.first_name = facebook_name
                user.email = facebook_email
                user.save()

                UserProfile.objects.create(up_id=facebook_user_id)


            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return Response(response_dict, status=200)


class UserProfileViewSet(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, **kwargs):
        request_d = request.data;
        user_id = request_d['user_id']

        get_queryset = UserProfile.objects.get(up_id=user_id)
        get_serializer_class = UserProfileSerializer(get_queryset, many=True)

        return Response(get_serializer_class.data, status=200)


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
            print(myuser)
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

        print("password:"+password);

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


