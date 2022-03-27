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
from . import my_settings as ms

import posts.views as postview
import users.views as userview


urlpatterns = [
    # path('admin', admin.site.urls),
    # path('user', include('users.urls')),
    #
    # path('search', include('search.urls')),
    # path('myPage', include('myPage.urls')),

    # board
    path('api/'+ms.API_SHA256_KEY+'board', postview.PostViewSet.as_view(), name='boardList'),
    path('api/'+ms.API_SHA256_KEY+'board/<int:b_id>', postview.PostDetailViewSet.as_view(), name='boardDetail'),
    path('api/'+ms.API_SHA256_KEY+'uploadImage', postview.UploadImageViewSet.as_view(), name='uploadImage'),
    path('api/'+ms.API_SHA256_KEY+'deleteImage', postview.DeleteImageViewSet.as_view(), name='deleteImage'),
    path('api/'+ms.API_SHA256_KEY+'board/updateviews', postview.PostDetailUpdateViewSet.as_view(), name='boardDetail'),

    path('api/'+ms.API_SHA256_KEY+'savePost', postview.SavePostViewSet.as_view(), name='savePost'),

    # searchPost
    path('api/'+ms.API_SHA256_KEY+'searchPost', postview.SearchPostViewSet.as_view(), name='searchPost'),

    # social login
    path('api/'+ms.API_SHA256_KEY+'socialLogin', userview.SocialLoginViewSet.as_view(), name='socialLogin'),  # post
    path('api/'+ms.API_SHA256_KEY+'logout', userview.LogoutUserViewSet.as_view(), name='userLogout'),  # get
    path('api/'+ms.API_SHA256_KEY+'userProfile', userview.UserProfileViewSet.as_view(), name='userProfile'),
    # path('api/'+ms.API_SHA256_KEY+'followUser', userview.FollowUserViewSet.as_view(), name='followUser'),

    # path('api/'+ms.API_SHA256_KEY+'register', userview.ResigterUserViewSet.as_view(), name='userRegister'),  # post
    # path('api/'+ms.API_SHA256_KEY+'login', userview.UserViewSet.as_view(), name='userLogin'),  # post

    # likepost(post)
    path('api/'+ms.API_SHA256_KEY+'likepost', postview.LikePostViewSet.as_view(), name='likePost'),

    # likepost(mypage, post)
    path('api/'+ms.API_SHA256_KEY+'mplikepost', postview.LikePostMpViewSet.as_view(), name='likePostMp'),

    # postComment
    path('api/'+ms.API_SHA256_KEY+'postcomment', postview.PostCommentViewSet.as_view(), name='postComment'),
    path('api/'+ms.API_SHA256_KEY+'postcomment/<int:pc_id>', postview.PostCommentDetailViewSet.as_view(), name='postCommentDetail'),

    # myPage
    path('api/'+ms.API_SHA256_KEY+'mypage', postview.MyPageViewSet.as_view(), name='myPage'),

    # followPage
    path('api/'+ms.API_SHA256_KEY+'followPost', postview.FollowPostViewSet.as_view(), name='followPost'),

    # getAddress
    path('api/'+ms.API_SHA256_KEY+'getSido', postview.GetSidoViewSet.as_view(), name='getSido'),
    path('api/'+ms.API_SHA256_KEY+'getSigungu', postview.GetSigunguViewSet.as_view(), name='getSigungu'),
    path('api/'+ms.API_SHA256_KEY+'getDong', postview.GetDongViewSet.as_view(), name='getDong'),

    # getReverseAddress
    path('api/'+ms.API_SHA256_KEY+'getReSido', postview.GetReSidoViewSet.as_view(), name='getReSido'),
    path('api/'+ms.API_SHA256_KEY+'getReSigungu', postview.GetReSigunguViewSet.as_view(), name='getReSigungu'),
    path('api/'+ms.API_SHA256_KEY+'getReDong', postview.GetReDongViewSet.as_view(), name='getReDong'),

    # path('accounts/', include('allauth.urls')),

] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
