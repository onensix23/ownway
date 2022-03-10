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

import posts.views as postview
import users.views as userview


urlpatterns = [
    # path('admin', admin.site.urls),
    # path('user', include('users.urls')),
    #
    # path('search', include('search.urls')),
    # path('myPage', include('myPage.urls')),

    # board
    path('api/board', postview.PostViewSet.as_view(), name='boardList'),
    path('api/board/<int:b_id>', postview.PostDetailViewSet.as_view(), name='boardDetail'),
    path('api/uploadImage', postview.ImageViewSet.as_view(), name='uploadImage'),
    path('api/board/updateviews', postview.PostDetailUpdateViewSet.as_view(), name='boardDetail'),

    # searchPost
    path('api/searchPost', postview.SearchPostViewSet.as_view(), name='searchPost'),

    # user login, logout, register

    # social login
    path('api/socialLogin', userview.SocialLoginViewSet.as_view(), name='socialLogin'),  # post
    path('api/logout', userview.LogoutUserViewSet.as_view(), name='userLogout'),  # get
    path('api/userProfile', userview.UserProfileViewSet.as_view(), name='userProfile'),

    # path('api/register', userview.ResigterUserViewSet.as_view(), name='userRegister'),  # post
    # path('api/login', userview.UserViewSet.as_view(), name='userLogin'),  # post

    # likepost(post)
    path('api/likepost', postview.LikePostViewSet.as_view(), name='likePost'),

    # likepost(mypage, post)
    path('api/mplikepost', postview.LikePostMpViewSet.as_view(), name='likePostMp'),

    # postComment
    path('api/postcomment', postview.PostCommentViewSet.as_view(), name='postComment'),
    path('api/postcomment/<int:b_id>', postview.PostCommentDetailViewSet.as_view(), name='postCommentDetail'),

    # myPage
    path('api/mypage', postview.MyPageViewSet.as_view(), name='myPage'),

    # followPage
    path('api/followPost', postview.FollowPostViewSet.as_view(), name='followPost'),

    # getAddress
    path('api/getSido', postview.GetSidoViewSet.as_view(), name='getSido'),
    path('api/getSigungu', postview.GetSigunguViewSet.as_view(), name='getSigungu'),
    path('api/getDong', postview.GetDongViewSet.as_view(), name='getDong'),

    # getReverseAddress
    path('api/getReSido', postview.GetReSidoViewSet.as_view(), name='getReSido'),
    path('api/getReSigungu', postview.GetReSigunguViewSet.as_view(), name='getReSigungu'),
    path('api/getReDong', postview.GetReDongViewSet.as_view(), name='getReDong'),

    # path('accounts/', include('allauth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
