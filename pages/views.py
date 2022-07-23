from django.http import HttpResponse
from django.shortcuts import render, redirect

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'main.html')