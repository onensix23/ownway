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
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

import posts.views as postview
import users.views as userview

router = routers.DefaultRouter()
# router.register(r'list', views.PostViewSet.as_view()) # board/list
# router.register(r'detail', views.PostViewSet)


urlpatterns = [
    #path('', include('mainP.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    # path('posts/', include('posts.urls')),
    path('search/', include('search.urls')),
    path('myPage/', include('myPage.urls')),
    path('board/', postview.PostViewSet.as_view(), name='boardList'),
    path('board/<int:b_id>', postview.PostDetailViewSet.as_view(), name='boardDetail'),

    # user login, logout, register
    path('login/', userview.UserViewSet.as_view(), name='userLogin'),
    path('logout/', userview.LogoutUserViewSet.as_view(), name='userLogout'),
    path('register/', userview.ResigterUserViewSet.as_view(), name='userRegister'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
