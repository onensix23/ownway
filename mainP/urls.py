from django.urls import path
from . import views
urlpatterns = [
   path('', views.mainPOpen), #즉, 최종적인 url은 127~~~~:8000/user/register가 된다.
   path('getSido', views.getSido, name='getSido'),
   
]