from django.urls import path
from . import views

urlpatterns = [
    path('', views.boardOpen, name="boardOpen"),
    path('boardInsert', views.boardInsert),
    path('boardDetail', views.boardDetail),
    path('boardEdit', views.boardEdit),
    path('boardDelete', views.boardDelete),
]