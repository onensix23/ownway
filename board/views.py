from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *


# Create your views here.


def boardOpen(request):
    all_board = Board.objects.all().order_by('-b_id').values()

    return render(request, 'board/read_board.html', {'all_board':all_board})


def boardInsert(request):
    """
        post
            - 넘어오는 것 : 아이디, 제목, 내용
            - 자동으로 채울 것 : 게시물 번호, 날짜, 좋아요 수 (0)
            - post 방식으로 받으면 insert 하고 read_page.html 로 redirect
    """
    if request.method == 'GET':
        return render(request,  'board/insert_board.html')

    elif request.method == 'POST':
        m_id = request.user.get_username()
        b_title = request.POST.get('b_title')
        b_text = request.POST.get('b_text')

        new_board = Board(m_id=m_id, b_title=b_title, b_text=b_text)

        new_board.save()  # insert

        return redirect('boardOpen')


def boardDetail(request):
    """
        boardList
            - b_id 갖고 get 으로 넘어옴
            - db select 모든거 갖고 옴
            - 내용 띄우고 db 에서 가져온 m_id랑 아이디 같으면 수정이나 삭제 버튼 생성
            - 아니라면 좋아요 버튼 보여줌

    """
    if request.method == 'GET':
        b_id = request.GET.get('b_id')

        # board_detail = Board.objects.filter(b_id=b_id)
        board_detail = Board.objects.get(b_id=b_id)

        return render(request, 'board/detail_board.html',{'board_detail':board_detail})


def boardEdit(request):
    if request.method == 'GET':
        b_id = request.GET.get('b_id_e')
        edit_board = Board.objects.get(b_id=b_id)
        print(b_id)
        return render(request, 'board/edit_board.html', {'edit_board': edit_board})

    if request.method == 'POST':
        b_id = request.POST.get('b_id')
        print(b_id)
        b_text = request.POST.get('b_text')
        b_title = request.POST.get('b_title')

        edit_board1 = Board.objects.get(b_id=b_id)
        edit_board1.b_title = b_title
        edit_board1.b_text = b_text

        edit_board1.save()
        return redirect('boardOpen')


def boardDelete(request):
    if request.method == 'POST':
        b_id = request.POST.get('b_id_d')
        Board.objects.get(b_id=b_id).delete()
        return redirect('boardOpen')

