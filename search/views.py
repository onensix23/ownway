import json
from django.http import HttpResponse
from posts.models import Posts
from django.shortcuts import render


def searchOpen(request):   #회원가입 페이지를 보여주기 위한 함수
    if request.method == "GET":
        return render(request, 'searchPage.html')


# def getSearch(request):
#     if request.method == "POST":
#         json_str = ((request.body).decode('utf-8'))
#         jsonObject = json.loads(json_str)
#
#         input_searchThing = jsonObject['searchThing']
#
#         #adm_dr = Posts.objects.filter(=sel_sigungu_cd).distinct().values('adm_dr_nm', 'adm_dr_cd2')  # 동
#         adm_dr_list = json.dumps(list(adm_dr))  # 시- 도 return
#
#         return HttpResponse(adm_dr_list, content_type="text/json-comment-filtered")