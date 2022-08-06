from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View

def AboutView(TemplateView):
    template_name='index_ee.html'
    # return HttpResponse("Hello, world. You're at the polls index.")
    # return render(request, 'index.html')
    
def index(request):
    return render(request, 'index.html')