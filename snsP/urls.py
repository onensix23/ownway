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
import terms.views as termsview
import reports.views as reportsview


urlpatterns = [
    path('', include('pages.urls')),

    # path('admin', admin.site.urls),
    path('terms/privacypolicy', termsview.PrivacyPolicyViewSet.as_view(), name='privacypolicy'), 
    path('terms/termsofservice', termsview.ServiceViewSet.as_view(), name='termsOfService'),

    path('test', postview.TestViewSet.as_view(), name='test'),
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
    path('api/'+ms.API_SHA256_KEY+'socialLogin', userview.SocialLoginViewSet.as_view(), name='socialLogin'), 

    #logout
    path('api/'+ms.API_SHA256_KEY+'logout', userview.LogoutUserViewSet.as_view(), name='userLogout'), 

    # resign 탈퇴 
    path('api/'+ms.API_SHA256_KEY+'resignUser', userview.ResignUserViewSet.as_view(), name='resignUser'),  
    path('api/'+ms.API_SHA256_KEY+'userData', userview.UserDataViewSet.as_view(), name='userData'), 

    # FCM Token 관리
    path('api/'+ms.API_SHA256_KEY+'userFCMToken', userview.UserFCMTokenViewSet.as_view(), name='userFCMToken'),

    path('api/'+ms.API_SHA256_KEY+'userNotification', userview.UserNotificationSet.as_view(), name='userProfile'),

    path('api/'+ms.API_SHA256_KEY+'userProfile', userview.UserProfileViewSet.as_view(), name='userProfile'),
    path('api/'+ms.API_SHA256_KEY+'followUser', userview.FollowUserViewSet.as_view(), name='followUser'),
    path('api/'+ms.API_SHA256_KEY+'blockUser', userview.BlockUserViewSet.as_view(), name='blockUser'),
    
    # likepost(post)
    path('api/'+ms.API_SHA256_KEY+'likepost', postview.LikePostViewSet.as_view(), name='likePost'),

    # likepost(mypage, post)
    path('api/'+ms.API_SHA256_KEY+'mplikepost', postview.LikePostMpViewSet.as_view(), name='likePostMp'),

    # postComment
    path('api/'+ms.API_SHA256_KEY+'postcomment', postview.PostCommentViewSet.as_view(), name='postComment'),
    # path('api/'+ms.API_SHA256_KEY+'postcomment/<int:pc_id>', postview.PostCommentDetailViewSet.as_view(), name='postCommentDetail'),

    # postPlace
    path('api/'+ms.API_SHA256_KEY+'postplace/<int:pp_id>', postview.PostPlaceViewSet.as_view(), name='postPlace'),
    path('api/'+ms.API_SHA256_KEY+'saveplace', postview.SavePostPlaceViewSet.as_view(), name='savePlace'),

    # myPage
    path('api/'+ms.API_SHA256_KEY+'mypage', postview.MyPageViewSet.as_view(), name='myPage'),

    # followPage
    path('api/'+ms.API_SHA256_KEY+'followPost', postview.FollowPostViewSet.as_view(), name='followPost'),

    path('api/'+ms.API_SHA256_KEY+'terms/howtodeletedata', termsview.HowToViewSet.as_view(), name='howtodeletedata'), 

    path('api/'+ms.API_SHA256_KEY+'reporttremplate', reportsview.ReportTemplateViewSet.as_view(), name='reporttremplate'),
    path('api/'+ms.API_SHA256_KEY+'report', reportsview.ReportViewSet.as_view(), name='report'),
    
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
