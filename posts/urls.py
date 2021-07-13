from django.urls import path, include
from . import views
import snsP.urls
from snsP.urls import router


urlpatterns = [
    # path('', views.PostViewSet.as_view(), name='boardList'),
    # path(r'^(?<b_id>\d+)/$', views.PostDetailViewSet.as_view(), name='boardDetail'),
    #

    # path('', views.boardOpen, name="boardOpen"),
    # path('boardInsert', views.boardInsert, name="boardInsert"),
    # path('boardDetail/<int:b_id>', views.boardDetail, name="boardDetail"),
    # path('boardEdit', views.boardEdit, name="boardEdit"),
    # path('boardDelete', views.boardDelete, name="boardDelete"),
    # path('getAddress',  views.getAddress, name="ajaxGetAdd"),
    # path('getSido', views.getSido, name='getSido'),
    # path('getGungu', views.getGungu, name='getGungu'),
    # path('getDong', views.getDong, name='getDong'),
    # path('test', include('rest_framework.urls', namespace="rest_framework_category")),
]