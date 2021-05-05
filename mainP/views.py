from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def mainPOpen(request):   #회원가입 페이지를 보여주기 위한 함수
    if request.method == "GET":
        return render(request, 'mainP.html')


def getSido(request):
    if request.method == "POST":
        #json_str = ((request.body).decode('utf-8'))
        #jsonObject = json.loads(json_str)
        #print(jsonObject)
        return JsonResponse({'title':'test'})
    