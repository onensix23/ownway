from django.urls import path
from . import views

urlpatterns = [
    path('', views.boardOpen, name="boardOpen"),
    path('boardInsert', views.boardInsert, name="boardInsert"),
    path('boardDetail/<int:b_id>', views.boardDetail, name="boardDetail"),
    path('boardEdit', views.boardEdit, name="boardEdit"),
    path('boardDelete', views.boardDelete, name="boardDelete"),
    path('getAddress',  views.getAddress, name="ajaxGetAdd"),
    path('getSido', views.getSido, name='getSido'),
    path('getGungu', views.getGungu, name='getGungu'),
    path('getDong', views.getDong, name='getDong'),
]