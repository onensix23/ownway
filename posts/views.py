from django.db.models.functions import Substr
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q,Subquery
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .serializers import *
from users.models import UserFollow
import json


class ImageViewSet(APIView):
    """
       POST /board/<b_id>
    """

    def post(self, request, **kwargs):
        # file1 = request.data['file1']
        # print(request.data)
        # print(request.data['b_id'])
        # print(request.FILES.keys())

        res_data = {
            "success": True,
            "error": None,
            "fileName": ''
        }

        postObj = Posts.objects.get(b_id=request.data['b_id'])

        if request.FILES:
            for k in request.FILES.keys():
                if k.find('uploadFile') != -1:
                    photo = Photo()
                    photo.b_id = postObj
                    photo.p_image = request.FILES[k]
                    request.FILES[k].name = photo.get_file_path(request.FILES[k].name)
                    photo.p_filename = request.FILES[k].name
                    photo.p_isthumb = request.data['type']

                    # 데이터베이스에 저장
                    photo.save()

                    res_data[k] = request.FILES[k].name

        return Response(res_data, status=200)


class PostViewSet(APIView):
    """
       POST /board/<b_id>
    """

    def post(self, request, **kwargs):
        res_data = {
            'post_success': False,
            'postcomment_success': 'no comment',
            'b_id': 6
        }

        print(request.data)

        user_id = request.data['user_id']
        b_title = request.data['b_title']
        b_address = request.data['b_address']
        b_theme = request.data['b_theme']
        b_hash_tag_1 = request.data['b_hash_tag_1']
        b_hash_tag_2 = request.data['b_hash_tag_2']
        b_place_id = request.data['b_place_id']

        pc_comment = request.data['pc_comment']

        print(request.data)

        userObj = User.objects.get(username=user_id)

        new_post = Posts(
                id=userObj, 
                b_title=b_title, 
                b_address=b_address,  
                b_theme=b_theme, 
                b_hash_tag_1=b_hash_tag_1, b_hash_tag_2=b_hash_tag_2, 
                b_place_id=b_place_id
        )

        new_post.save()  # insert
        res_data['post_success']=True
        
        print(new_post.b_id)

        res_data['b_id'] = new_post.b_id
        postObj = Posts.objects.get(b_id=new_post.b_id)
        print(postObj)

        if pc_comment != '':
            new_postcomment = PostComment(
                b_id=postObj,
                id=userObj,
                pc_comment=pc_comment,
                pc_type='1'
            )

            new_postcomment.save()
            res_data['postcommet_success']=True


        return Response(res_data, status=200)

    """
    GET /board
        detail (b_id)
    """
    def get(self, request, **kwargs):

        if(len(request.GET) > 0): #detail
            # print('1')
            get_queryset = Posts.objects.prefetch_related('photo_b_id').prefetch_related('postcomment_b_id').filter(Q(
                Q(b_id=request.GET['b_id'])
            )).select_related('id')
            get_serializer_class = PostSerializer(get_queryset, many=True)

        else:
            # print('2')
            get_queryset = Posts.objects.prefetch_related('photo_b_id').filter(Q(
                Q(photo_b_id__p_isthumb='1') | Q(photo_b_id=None)
            )).select_related('id')

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

        if request.data['v_b_text'] == 990622:
            b_id = request.data['b_id']
            queryset = Posts.objects.get(b_id=b_id)
            queryset.b_del = 'Y'
            queryset.save()
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
        search_text = request.data['search_text']
        get_queryset = Posts.objects.filter(b_title__icontains=search_text)
        get_serializer_class = PostDetailSerializer(get_queryset, many=True)

        return Response(get_serializer_class.data, status=200)


class LikePostViewSet(APIView):
    """
    GET, POST /likepost/
    """

    def post(self, request, **kwargs):
        res_data = {
            "success": True,
            "error": None
        }
        if request.data['type'] == 0:
            # select
            user_id = request.data['userId']
            b_id = request.data['b_id']

            # print('userId')
            # print(user_id)
            # print('b_id')
            # print(b_id)

            get_queryset = LikePost.objects.filter(id=user_id, b_id=b_id)
            get_serializer_class = IsLikePostSerializer(get_queryset, many=True)

            # print(get_serializer_class.data)
            return Response(get_serializer_class.data, status=200)

        else:
            user_id = request.data['userId']
            b_id = request.data['b_id']

            get_queryset = LikePost.objects.filter(id=user_id, b_id=b_id).count()

            print(get_queryset)

            if get_queryset == 0:
                # insert
                sel_post = Posts.objects.get(b_id=b_id)
                sel_user = User.objects.get(username=user_id)

                # new_likepost = LikePost(id=user_id, b_id=b_id)
                LikePost.objects.create(
                    id=sel_user,
                    b_id=sel_post,
                )

            else:
                # update
                uLikePost = LikePost.objects.get(id=user_id, b_id=b_id)

                if uLikePost.lp_del == "Y":
                    uLikePost.lp_del = "N"
                else:
                    uLikePost.lp_del = "Y"

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


class MyPageViewSet(APIView):
    """
    POST /mypage/
    """

    def post(self, request, **kwargs):
        user_id = request.data['userId']
        get_queryset = Posts.objects.filter(id=user_id, b_del='N')
        get_serializer_class = PostDetailSerializer(get_queryset, many=True)
        # print(get_serializer_class.data)
        return Response(get_serializer_class.data, status=200)


class FollowPostViewSet(APIView):
    """
    POST /followPost/
    """
    def post(self, request, **kwargs):
        user_id = request.data['userId']

        get_queryset = Posts.objects.filter(id__in=Subquery(UserFollow.objects.values('uf_reading').filter(uf_reader=user_id)), b_del='N').order_by('-b_datetime')
        get_serializer_class = PostDetailSerializer(get_queryset, many=True)

        return Response(get_serializer_class.data, status=200)

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


class PostCommentDetailViewSet(RetrieveAPIView):
    lookup_field = 'b_id'
    queryset = PostComment.objects.all().order_by('-pc_datetime')
    serializer_class = PostCommentSerializer


class PostUpdateViewSet(UpdateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostDetailSerializer


class PostDeleteViewSet(DestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostDetailSerializer


def boardOpen(request):
    all_board = Posts.objects.all().order_by('-b_id').values()

    photo1 = Posts.objects.select_related().order_by(
        '-b_id'
    ).values('b_title', 'b_id', 'b_datetime', 'b_locType1', 'b_locType2', 'b_locType3')

    print(all_board)
    return render(request, 'board/read_board.html', {'all_board': all_board})


def boardInsert(request):
    """
        post
            - 넘어오는 것 : 아이디, 제목, 내용
            - 자동으로 채울 것 : 게시물 번호, 날짜, 좋아요 수 (0)
            - post 방식으로 받으면 insert 하고 read_page.html 로 redirect
    """
    if request.method == 'GET':
        form1 = CreatePost()
        form2 = CreatePhoto()
        return render(request, 'board/insert_board_loc.html', {'form1': form1, 'form2': form2})
        # return render(request,  'board/insert_board.html')

    elif request.method == 'POST':
        user_id = request.user.get_username()
        b_title = request.POST.get('title1')
        b_text = request.POST.get('content1')
        b_locType1 = request.POST.get('sido1')
        b_locType2 = request.POST.get('gungu1')
        b_locType3 = request.POST.get('dong1')
        b_theme = request.POST.get('theme1')

        print(b_title)
        print(b_text)
        print(b_locType1)
        print(b_locType2)
        print(b_locType3)
        print(b_theme)

        new_post = Posts(user_id=user_id, b_title=b_title, b_text=b_text,
                         b_locType1=b_locType1, b_locType2=b_locType2, b_locType3=b_locType3,
                         b_theme=b_theme)

        new_post.save()  # insert
        print(request.FILES.keys())
        if request.FILES:
            if 'file1' in request.FILES.keys():
                # Photo 객체를 하나 생성한다.
                photo = Photo()
                # 외래키로 현재 생성한 Post의 기본키를 참조한다.
                photo.post = new_post
                photo.image = request.FILES['file1']
                request.FILES['file1'].name = photo.get_file_path(request.FILES['file1'].name)
                photo.filename = request.FILES['file1'].name
                # 데이터베이스에 저장
                photo.save()

        # for img in request.FILES.getlist('imgs'):
        #     # Photo 객체를 하나 생성한다.
        #     photo = Photo()
        #     # 외래키로 현재 생성한 Post의 기본키를 참조한다.
        #     photo.post = new_post
        #     # imgs로부터 가져온 이미지 파일 하나를 저장한다.
        #     photo.image = img
        #     # 파일명 변경
        #     photo.filename = img.name
        #
        #     # 데이터베이스에 저장
        #     photo.save()

        return redirect('boardOpen')


def boardDetail(request, b_id):
    """
        boardList
            - b_id 갖고 get 으로 넘어옴
            - db select 모든거 갖고 옴
            - 내용 띄우고 db 에서 가져온 m_id랑 아이디 같으면 수정이나 삭제 버튼 생성
            - 아니라면 좋아요 버튼 보여줌

    """
    if request.method == 'GET':
        # b_id = request.GET.get('b_id')

        # board_detail = Board.objects.filter(b_id=b_id)
        # board_detail = Posts.objects.get(b_id=b_id)
        board_detail = Posts.objects.select_related().get(b_id=b_id)
        board_photo = Photo.objects.get(post_id=b_id)
        return render(request, 'board/detail_board.html', {'board_detail': board_detail, 'board_photo': board_photo})


def boardEdit(request):
    if request.method == 'GET':
        b_id = request.GET.get('b_id_e')
        edit_board = Posts.objects.get(b_id=b_id)
        print(b_id)
        return render(request, 'posts/edit_board.html', {'edit_board': edit_board})

    if request.method == 'POST':
        b_id = request.POST.get('b_id')
        print(b_id)
        b_text = request.POST.get('b_text')
        b_title = request.POST.get('b_title')

        edit_board1 = Posts.objects.get(b_id=b_id)
        edit_board1.b_title = b_title
        edit_board1.b_text = b_text

        edit_board1.save()
        return redirect('boardOpen')


def boardDelete(request):
    if request.method == 'POST':
        b_id = request.POST.get('b_id_d')
        Posts.objects.get(b_id=b_id).delete()
        return redirect('boardOpen')


def getAddress(request):
    if request.method == 'POST':
        b_id = request.POST.get('b_id_d')
        Posts.objects.get(b_id=b_id).delete()
        return redirect('boardOpen')


def getSido(request):
    if request.method == "POST":
        jsonObject = json.loads(request.body)
        # select distinct(sido_nm,sido_cd) from KoreaDongPgTbl
        # sido = KoreaDongPgTbl.objects.filter().distinct().values('sido_nm', 'sido_cd')
        # sido = EntrcSido.objects.filter(sido_nm=F('sido_nm'),doro_cd=F(Substr('doro_cd', 1, 2))).distinct()
        # sido = EntrcSido.objects.annotate(doro_cd1=(Substr('doro_cd', 1, 2))).values('sido_nm', 'doro_cd').distinct()
        # sido = EntrcSido.objects.filter(sido_nm=F('sido_nm'), doro_cd=(Substr('doro_cd', 1, 2))).values('sido_nm', 'doro_cd').distinct()
        # sido = EntrcSido.objects.raw('select l.sido_cd, l.sido_nm from ( select distinct(sido_nm) as sido_nm, substr(doro_cd,1,2) as sido_cd  from ownway.entrc_sido)l')
        # sido = EntrcSido.objects.annotate(doro_cd1=(Substr('doro_cd', 1, 2))).distinct().values('sido_nm', 'doro_cd')

        sido = EntrcSido.objects.values('sido_nm').annotate(sido_cd=(Substr('doro_cd', 1, 2))).distinct()
        # select distinct(sido_nm) as sido_nm, substr(doro_cd,1,2) as sido_cd from ownway.entrc_sido;

        # print(sido.query)
        # print(sido)
        # = KoreaDongPgTbl.objects.filter().distinct().values('sido_nm', 'sido_cd')
        sido_list = json.dumps(list(sido))  # 시- 도 return
        # print(sido_list)
        return HttpResponse(sido_list, content_type="text/json-comment-filtered")


def getGungu(request):
    if request.method == "POST":
        json_str = ((request.body).decode('utf-8'))
        jsonObject = json.loads(json_str)

        sel_sido_cd = jsonObject['sido_cd']

        # sigungu = KoreaDongPgTbl.objects.filter(sido_cd=sel_sido_cd).distinct().values('sigungu_nm', 'sigungu_cd')

        # SELECT DISTINCT(sigungu_nm) ,SUBSTR(doro_cd,3,3) FROM entrc_sido WHERE DORO_CD LIKE '11%';
        sigungu = EntrcSido.objects.values('sigungu_nm').annotate(
            sigungu_cd=(Substr('doro_cd', 3, 3))).distinct().filter(doro_cd__startswith=sel_sido_cd)
        sigungu_list = json.dumps(list(sigungu))  # 시- 도 return
        # print(sigungu_list)
        # print(sigungu.query)
        return HttpResponse(sigungu_list, content_type="text/json-comment-filtered")


def getDong(request):
    if request.method == "POST":
        json_str = ((request.body).decode('utf-8'))
        jsonObject = json.loads(json_str)

        sel_gun_do_cd = str(jsonObject['sido_cd']) + str(jsonObject['sigungu_cd'])

        print(sel_gun_do_cd)
        # adm_dr = KoreaDongPgTbl.objects.filter(sigungu_cd=sel_sigungu_cd).distinct().values('adm_dr_nm', 'adm_dr_cd2')  # 동
        # SELECT DISTINCT(dong_nm) ,SUBSTR(doro_cd,3,3) FROM entrc_sido WHERE DORO_CD LIKE '11110%' AND dong_one_cd != '00' order by doro_cd, dong_one_cd;
        qes1 = ~Q(dong_one_cd='00')
        dong = EntrcSido.objects.values('dong_nm', 'dong_cd').distinct().filter(
            doro_cd__startswith=sel_gun_do_cd).filter(qes1)

        dong_list = json.dumps(list(dong))  # 시- 도 return
        print(dong.query)
        # rint(dong_list)
        return HttpResponse(dong_list, content_type="text/json-comment-filtered")
