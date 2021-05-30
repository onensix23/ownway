from django.db.models.functions import Concat
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import json
from django.http import HttpResponse
from django.db.models import Q, FilteredRelation, Value
from posts.models import Posts, Photo


# Create your views here.
def myPageOpen(request):   #회원가입 페이지를 보여주기 위한 함수
    if request.method == "GET":
        user = request.user.get_username()
        if not user:  # 로그인 하지 않았다면
            return redirect('login')
        else:
            #filter(user_id=user).order_by('-b_id')
            #post1 = Posts.objects.filter(user_id=user).order_by('-b_id')
            #print(post1.query)
            #print(post1)
            #post_id_list = []
            #for  post_id_list.append(i.b_id) i in post1:
             #
            #photo1 = Photo.objects.filter(post_id__in=post_id_list).order_by('-id')

            # post1 = Posts.objects.filter(user_id=user).order_by('-b_id')
            # post_id_list = []
            # for i in post1:
            #     post_id_list.append(i.b_id)
            # photo1 = Photo.objects.filter(post_id__in=post_id_list).order_by('-id')
            # print(photo1)
            # print(photo1[0].post_id.b_text)
            # return render(request, 'myPage.html', {'photo1': photo1})

            #photo1 = Photo.objects.select_related().filter(id=11).order_by('-post_id')
            # photo1 = Photo.objects.select_related().filter(posts_posts__in=user).order_by('-post_id')
            #
            # print(photo1.query)
            # print(photo1)
            #a = Photo.objects.annotate(has_tag=FilteredRelation('post_id'),condition=Q(post__user_id=user)).order_by('-post_id')
            #print(a.query)

            """
            SELECT `posts_photo`.`id`, `posts_photo`.`post_id`, `posts_photo`.`image`, `posts_photo`.`filename`,
                    `posts_posts`.`b_id`, `posts_posts`.`user_id`, `posts_posts`.`b_locType1`, 
                    `posts_posts`.`b_locType2`, `posts_posts`.`b_locType3`, `posts_posts`.`b_theme`, 
                    `posts_posts`.`b_title`, `posts_posts`.`b_text`, `posts_posts`.`b_datetime` 
            FROM `posts_photo` INNER JOIN `posts_posts` ON (`posts_photo`.`post_id` = `posts_posts`.`b_id`) 
            WHERE `posts_posts`.`user_id` = rohhj622 
            ORDER BY `posts_photo`.`post_id` DESC"""

            photo1 = Photo.objects.select_related().filter(
                post__user_id=user
            ).order_by(
                '-post_id'
            ).values('image','post__b_title','post__b_text','post__b_locType1','post__b_locType2', 'post__b_locType3')

            print(photo1.query)

            print(photo1)
            return render(request, 'myPage.html', {'photo1': photo1})