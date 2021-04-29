from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *


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
        return render(request, 'board/insert_board_loc.html')
        # return render(request,  'board/insert_board.html')

    elif request.method == 'POST':
        user_id = request.user.get_username()
        b_title = request.POST.get('b_title')
        b_text = request.POST.get('b_text')

        new_post = Posts(user_id=user_id, b_title=b_title, b_text=b_text)

        new_post.save()  # insert

        if request.FILES:
            if 'imgs' in request.FILES.keys():
                # Photo 객체를 하나 생성한다.
                photo = Photo()
                # 외래키로 현재 생성한 Post의 기본키를 참조한다.
                photo.post = new_post
                photo.image = request.FILES['imgs']
                request.FILES['imgs'].name = photo.get_file_path(request.FILES['imgs'].name)
                photo.filename = request.FILES['imgs'].name
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

