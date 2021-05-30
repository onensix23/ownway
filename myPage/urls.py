from django.urls import path
from . import views

urlpatterns = [
   path('', views.myPageOpen), #즉, 최종적인 url은 127~~~~:8000/user/register가 된다.
   
]