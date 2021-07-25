from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# 비밀번호 암호화 / 패스워드 체크(db에있는거와 일치성확인)
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .serializers import UserSerializer
# Create your views here.


class UserViewSet(APIView):
    """
       POST /user
       """

    def post(self, request, **kwargs):
        response_data = {}
        login_username = request.POST.get('userId', None)
        login_password = request.POST.get('userPassword', None)

        print(login_username, login_password)
        if not (login_username and login_password):
            response_data['error'] = "아이디와 비밀번호를 모두 입력해주세요."
        else:
            myuser = authenticate(username=login_username, password=login_password)
            # db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.
            print(myuser)
            if myuser is not None:
                login(request, myuser)
                # request.session['user'] = myuser.username
                #     # 세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                #     # 세션 user라는 key에 방금 로그인한 id를 저장한것.
                return redirect('/')
            else:
                response_data['error'] = "비밀번호를 틀렸습니다."


        b_id = kwargs.get('b_id')
        get_queryset = UserSerializer.objects.get(username=login_username)
        get_serializer_class = UserSerializer(get_queryset)
        return Response(get_serializer_class.data, status=200)

    """
    GET /user
    GET /user/{user_id}
    """

    # def get(self, request,  **kwargs):
    #     if(kwargs.get('b_id') is None):
    #         get_queryset = Posts.objects.all()
    #         get_serializer_class = PostDetailSerializer(get_queryset, many=True)
    #         return Response(get_serializer_class.data, status=200)
    #     else:
    #         b_id = kwargs.get('b_id')
    #         get_queryset = Posts.objects.get(b_id=b_id)
    #         get_serializer_class = PostDetailSerializer(get_queryset)
    #         return Response(get_serializer_class.data, status=200)
    # def get(self, request,  **kwargs):
    #     get_queryset = Posts.objects.all()
    #     get_serializer_class = PostDetailSerializer(get_queryset, many=True)
    #     return Response(get_serializer_class.data, status=200)

    """
        PUT /board/{b_id}
    """
    # def put(self, request):
    #     post_serializer = PostDetailSerializer(data=request.data)  # Request의 data를 Serializer로 변환
    #     return Response(post_serializer.data, status=status.HTTP_201_CREATED)  # client에게 JSON response 전달

    """
    DELETE /user/{user_id}
    """
    # def delete(self, request, **kwargs):
    #
    #     if(kwargs.get('b_id') is None):
    #         return Response("nothing happend", status=200)
    #     else:
    #         b_id = kwargs.get('b_id')
    #         queryset = Posts.objects.get(b_id=b_id)
    #         queryset.b_del = 'Y'
    #         queryset.save()
    #         return Response("deleted", status=200)



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
            m_password = make_password(password, None, 'pbkdf2_sha256')
            user = User.objects.create_user(username=id1, password=m_password,
                                            first_name=nickname, email=email)
            res_data['success'] = "가입되었습니다."

        return render(request, 'register.html', res_data) #register를 요청받으면 register.html 로 응답.


@csrf_exempt
def signin(request):
    response_data = {}
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        login_username = request.POST.get('userId', None)
        login_password = request.POST.get('userPassword', None)

        print(login_username, login_password)
        if not (login_username and login_password):
            response_data['error'] = "아이디와 비밀번호를 모두 입력해주세요."
        else:
            myuser = authenticate(username=login_username, password=login_password)
            # db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.
            print(myuser)
            if myuser is not None:
                login(request, myuser)
                # request.session['user'] = myuser.username
                #     # 세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                #     # 세션 user라는 key에 방금 로그인한 id를 저장한것.
                return redirect('/')
            else:
                response_data['error'] = "비밀번호를 틀렸습니다."
        print('ihi');
        return Response(response_data['error'], status=200)
        # return render(request, 'login.html', response_data)

#
# def signin(request):
#     response_data = {}
#     if request.method == "GET":
#         return render(request, 'login.html')
#     elif request.method == "POST":
#         login_username = request.POST.get('id', None)
#         login_password = request.POST.get('password', None)
#
#         print(login_username, login_password)
#         if not (login_username and login_password):
#             response_data['error'] = "아이디와 비밀번호를 모두 입력해주세요."
#         else:
#             myuser = authenticate(username=login_username, password=login_password)
#             # db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.
#             print(myuser)
#             if myuser is not None:
#                 login(request, myuser)
#                 # request.session['user'] = myuser.username
#                 #     # 세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
#                 #     # 세션 user라는 key에 방금 로그인한 id를 저장한것.
#                 return redirect('/')
#             else:
#                 response_data['error'] = "비밀번호를 틀렸습니다."
#
#         return render(request, 'login.html', response_data)


def home(request):
    user_id = request.session.get('user')
    if user_id:
        myuser_info = User.objects.filter(username=user_id)  # pk : primary key
        return HttpResponse(myuser_info.username)  # 로그인을 했다면, username 출력

    return HttpResponse('로그인을 해주세요.')  # session에 user가 없다면, (로그인을 안했다면)


def signout(request):
    logout(request)
    response = redirect('/')
    response.delete_cookie('user_location')
    # request.session.pop('user')
    return redirect('/')



