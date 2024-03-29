import json, requests, subprocess
import threading

from django.core.paginator import Paginator

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# 비밀번호 암호화 / 패스워드 체크(db에있는거와 일치성확인)
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.db.models import F

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
        elif request_d['socialType'] == 'apple':
            if request_d['type'] == 'login':
                response_dict = request_d['data']
                
                apple_user_id = response_dict['user']
                apple_name = '무직1'

                if 'email' in response_dict.keys():
                    apple_email = response_dict['email']
                else:
                    apple_email = ''

                user, user_created = User.objects.get_or_create(username=apple_user_id)

                # 유저가 새로 생성되었다면
                if user_created:
                    user.first_name = apple_name
                    user.email = apple_email
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
    @method_decorator(csrf_exempt)
    def post(self, request, **kwargs):

        res_data = {
            "action" : "create",
            "count" : 0,
            "is_following" : True,
            "success" : True
        }

        if 'post_type' in request.data:
            user_id = request.data['user_id']
            userObj = User.objects.get(username=user_id)
            
            page_host = request.data['page_host']
            type = request.data['type']
            
            if type == 'reading':
                temp = UserFollow.objects.filter(uf_reading=page_host).values('uf_reader')
                
                readingObj = User.objects.filter(Q(~Q(username__in=Subquery(UserBlock.objects.values('ub_to').filter(ub_from=userObj)))&Q(username__in=temp))) #.order_by(F('username').desc(nulls_first=True)) # 따라가는 사람 # ~Q(username__in=Subquery(UserBlock.objects.values('ub_to').filter(ub_from=userObj))) and 
                serialize_data = UserSerializer3(readingObj, many=True, context={'user_id': user_id, 'type' : 'reader'})
                res_data = sorted(serialize_data.data, key=lambda k: k['is_already_follow'], reverse=False)

            elif type == 'reader':
                temp = UserFollow.objects.filter(uf_reader=page_host).values('uf_reading')
                
                readerObj = User.objects.filter(Q(~Q(username__in=Subquery(UserBlock.objects.values('ub_to').filter(ub_from=userObj))) & Q(username__in=temp))) #따라오게 하는 사람 ~Q(username__in=Subquery(UserBlock.objects.values('ub_to').filter(ub_from=userObj))) and
                serialize_data = UserSerializer3(readerObj, many=True, context={'user_id': user_id, 'type' : 'reader'})
                res_data = sorted(serialize_data.data, key=lambda k: k['is_already_follow'], reverse=False)

            return Response(res_data, status=200)
        
        else:
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

class UserNotiControllSet(APIView):
    def post(self, request, **kwargs):
        res_data = {
            'success': True,
            'error': None,
            'action' : '',
            'result' : '',
        }
        
        c_value = request.data['value']
        type = request.data['type']
        userObj = User.objects.get(username=request.data['user_id'])
        userFcmObj = UserFCMToken.objects.filter(ufcm_user_id=userObj)
        
        try:
            if type == 'pc_c':
                userFcmObj.update(ufcm_pc_c=c_value)
            elif type == 'sp_c':
                userFcmObj.update(ufcm_sp_c=c_value)
            elif type == 'fu_c':
                userFcmObj.update(ufcm_fu_c=c_value)
            elif type == 'pc_u':
                userFcmObj.update(ufcm_pc_u=c_value)
            elif type == 'pp_c':
                userFcmObj.update(ufcm_pp_c=c_value)
            elif type == 'im_c':
                userFcmObj.update(ufcm_im_c=c_value)
                
        except Exception as e:
            print(e)
            res_data['error'] = e
            res_data['success'] = False
                
        return Response(res_data, status=200)
        
class UserNotificationSet(APIView):

    def post(self, request, **kwargs):
        res_data = {
            'success': False,
            'error': None,
            'action' : '',
            'result' : '',
        }
        
        user_id = request.data['userId']
        device_id = request.data['deviceId']
        token = request.data['token']

        if 'type' in request.data:
            userObj = User.objects.get(username=user_id)
            userFCMObj = UserFCMToken.objects.get(ufcm_user_id=userObj,ufcm_device_id=device_id,ufcm_token=token)

            userNotificationObj = UserNotification.objects.filter(un_token_id=userFCMObj, un_to=userObj, un_is_sended=True, un_is_read=False).count()
            # print(userNotificationObj)
            res_data['result'] = userNotificationObj
            
            return Response(res_data, status=200)
            
        else:
            userObj = User.objects.get(username=user_id)
            userFCMObj = UserFCMToken.objects.get(ufcm_user_id=userObj,ufcm_device_id= device_id,ufcm_token=token)

            try:
                userNotificationObj = UserNotification.objects.filter(un_token_id=userFCMObj,un_to=userObj, un_is_sended=True).order_by("-un_send_date")
                
                paginator = Paginator(userNotificationObj, 15)
                page = request.data['page']
            
                if paginator.num_pages < page:
                    res_data = None
                else:   
                    posts = paginator.get_page(page)
                    get_serializer_class = UserNotificationSerializer2(posts, many=True)
                    res_data = get_serializer_class.data
                    
                return Response(res_data, status=200)

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


##########################################################################################

def register(request):   #회원가입 페이지를 보여주기 위한 함수
    if request.method == "GET":
        return render(request, 'register.html')

    elif request.method == "POST":
        id1 = request.POST.get('id1')   #딕셔너리형태
        password = request.POST.get('password')
        nickname = request.POST.get('nickname')
        email = request.POST.get('email')
        re_password = request.POST.get('re_password')
        res_data = {}

        if not (id1 and password and re_password and email and nickname):
            res_data['error1'] = "모든 값을 입력해야 합니다."
        elif password != re_password:
            # return HttpResponse('비밀번호가 다릅니다.')
            res_data['error2'] = '비밀번호가 다릅니다.'
        elif (User.objects.filter(username=id1)).count() != 0:
            res_data['error3'] = '중복된 ID 입니다.'
        else:
            # username id ,
            user = User.objects.create_user(username=id1, password=password,
                                            first_name=nickname, email=email)
            res_data['success'] = "가입되었습니다."

        return render(request, 'register.html', res_data) #register를 요청받으면 register.html 로 응답.


def signin(request):
    response_data = {}
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        login_username = request.POST.get('id', None)
        login_password = request.POST.get('password', None)


        if not (login_username and login_password):
            response_data['error'] = "아이디와 비밀번호를 모두 입력해주세요."
        else:
            myuser = authenticate(username=login_username, password=login_password)
            # db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.

            if myuser is not None:
                login(request, myuser)
                # request.session['user'] = myuser.username
                #     # 세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                #     # 세션 user라는 key에 방금 로그인한 id를 저장한것.
                return redirect('/')
            else:
                response_data['error'] = "비밀번호를 틀렸습니다."

        return render(request, 'login.html', response_data)


def home(request):
    user_id = request.session.get('user')
    if user_id:
        myuser_info = User.objects.filter(username=user_id)  # pk : primary key
        return HttpResponse(myuser_info.username)  # 로그인을 했다면, username 출력

    return HttpResponse('로그인을 해주세요.')  # session에 user가 없다면, (로그인을 안했다면)


def signout(request):
    logout(request)
    # request.session.pop('user')
    return redirect('/')