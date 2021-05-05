from django.shortcuts import render


def mainPOpen(request):   #회원가입 페이지를 보여주기 위한 함수
    if request.method == "GET":
        return render(request, 'mainP.html')

