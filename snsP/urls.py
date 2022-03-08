"""snsP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
import django.contrib.auth.urls
import social_django.urls

import posts.views as postview
import users.views as userview

router = routers.DefaultRouter()
# router.register(r'list', views.PostViewSet.as_view()) # board/list
# router.register(r'detail', views.PostViewSet)



urlpatterns = [
    # path('admin', admin.site.urls),
    # path('user', include('users.urls')),
    #
    # path('search', include('search.urls')),
    # path('myPage', include('myPage.urls')),


    # board
    path('board', postview.PostViewSet.as_view(), name='boardList'),
    path('board/<int:b_id>', postview.PostDetailViewSet.as_view(), name='boardDetail'),
    path('uploadImage', postview.ImageViewSet.as_view(), name='uploadImage'),
    path('board/updateviews', postview.PostDetailUpdateViewSet.as_view(), name='boardDetail'),

    # searchPost
    path('searchPost', postview.SearchPostViewSet.as_view(), name='searchPost'),

    # user login, logout, register

    # social login
    path('socialLogin', userview.SocialLoginViewSet.as_view(), name='socialLogin'),  # post
    path('logout', userview.LogoutUserViewSet.as_view(), name='userLogout'),  # get
    path('userProfile', userview.UserProfileViewSet.as_view(), name='userProfile'),

    # path('register', userview.ResigterUserViewSet.as_view(), name='userRegister'),  # post
    # path('login', userview.UserViewSet.as_view(), name='userLogin'),  # post

    # likepost(post)
    path('likepost', postview.LikePostViewSet.as_view(), name='likePost'),

    # likepost(mypage, post)
    path('mplikepost', postview.LikePostMpViewSet.as_view(), name='likePostMp'),

    # postComment
    path('postcomment', postview.PostCommentViewSet.as_view(), name='postComment'),
    path('postcomment/<int:b_id>', postview.PostCommentDetailViewSet.as_view(), name='postCommentDetail'),

    # myPage
    path('mypage', postview.MyPageViewSet.as_view(), name='myPage'),

    # getAddress
    path('getSido', postview.GetSidoViewSet.as_view(), name='getSido'),
    path('getSigungu', postview.GetSigunguViewSet.as_view(), name='getSigungu'),
    path('getDong', postview.GetDongViewSet.as_view(), name='getDong'),

    # getReverseAddress
    path('getReSido', postview.GetReSidoViewSet.as_view(), name='getReSido'),
    path('getReSigungu', postview.GetReSigunguViewSet.as_view(), name='getReSigungu'),
    path('getReDong', postview.GetReDongViewSet.as_view(), name='getReDong'),

    # path('accounts/', include('allauth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
