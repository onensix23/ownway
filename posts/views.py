from django.db.models.functions import Substr
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
import json
from django.http import HttpResponse
from django.core import serializers
from .models import KoreaDongPgTbl, EntrcSido
from django.db.models import F
from django.db.models import Q

# Create your views here.


def boardOpen(request):
    all_board = Posts.objects.all().order_by('-b_id').values()

    return render(request, 'board/read_board.html', {'all_board':all_board})


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
        #board_detail = Posts.objects.get(b_id=b_id)
        board_detail = Posts.objects.select_related().get(b_id=b_id)
        board_photo = Photo.objects.get(post_id=b_id)
        return render(request, 'board/detail_board.html', {'board_detail':board_detail, 'board_photo':board_photo})


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
        #sido = EntrcSido.objects.annotate(doro_cd1=(Substr('doro_cd', 1, 2))).values('sido_nm', 'doro_cd').distinct()
        #sido = EntrcSido.objects.filter(sido_nm=F('sido_nm'), doro_cd=(Substr('doro_cd', 1, 2))).values('sido_nm', 'doro_cd').distinct()
        #sido = EntrcSido.objects.raw('select l.sido_cd, l.sido_nm from ( select distinct(sido_nm) as sido_nm, substr(doro_cd,1,2) as sido_cd  from ownway.entrc_sido)l')
        # sido = EntrcSido.objects.annotate(doro_cd1=(Substr('doro_cd', 1, 2))).distinct().values('sido_nm', 'doro_cd')

        sido = EntrcSido.objects.values('sido_nm').annotate(sido_cd=(Substr('doro_cd', 1, 2))).distinct()
        # select distinct(sido_nm) as sido_nm, substr(doro_cd,1,2) as sido_cd from ownway.entrc_sido;

        #print(sido.query)
        #print(sido)
        # = KoreaDongPgTbl.objects.filter().distinct().values('sido_nm', 'sido_cd')
        sido_list = json.dumps(list(sido))  # 시- 도 return
        #print(sido_list)
        return HttpResponse(sido_list, content_type="text/json-comment-filtered")


def getGungu(request):
    if request.method == "POST":
        json_str = ((request.body).decode('utf-8'))
        jsonObject = json.loads(json_str)

        sel_sido_cd = jsonObject['sido_cd']

        #sigungu = KoreaDongPgTbl.objects.filter(sido_cd=sel_sido_cd).distinct().values('sigungu_nm', 'sigungu_cd')

        # SELECT DISTINCT(sigungu_nm) ,SUBSTR(doro_cd,3,3) FROM entrc_sido WHERE DORO_CD LIKE '11%';
        sigungu = EntrcSido.objects.values('sigungu_nm').annotate(sigungu_cd=(Substr('doro_cd', 3, 3))).distinct().filter(doro_cd__startswith=sel_sido_cd)
        sigungu_list = json.dumps(list(sigungu))  # 시- 도 return
        # print(sigungu_list)
        # print(sigungu.query)
        return HttpResponse(sigungu_list, content_type="text/json-comment-filtered")


def getDong(request):
    if request.method == "POST":
        json_str = ((request.body).decode('utf-8'))
        jsonObject = json.loads(json_str)
        
        sel_gun_do_cd = str(jsonObject['sido_cd'])+ str(jsonObject['sigungu_cd'])

        print(sel_gun_do_cd)
        #adm_dr = KoreaDongPgTbl.objects.filter(sigungu_cd=sel_sigungu_cd).distinct().values('adm_dr_nm', 'adm_dr_cd2')  # 동
        #SELECT DISTINCT(dong_nm) ,SUBSTR(doro_cd,3,3) FROM entrc_sido WHERE DORO_CD LIKE '11110%' AND dong_one_cd != '00' order by doro_cd, dong_one_cd;
        qes1 = ~Q(dong_one_cd='00')
        dong = EntrcSido.objects.values('dong_nm','dong_cd').distinct().filter(doro_cd__startswith=sel_gun_do_cd).filter(qes1)

        dong_list = json.dumps(list(dong))  # 시- 도 return
        print(dong.query)   
        #rint(dong_list)
        return HttpResponse(dong_list, content_type="text/json-comment-filtered")

