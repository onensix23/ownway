from django.shortcuts import render
from django.db.models import Q,Subquery
from firebase_admin import messaging
import json, requests, timeit, asyncio

from datetime import datetime, timedelta

from .models  import *
from users.serializers import UserFCMTokenSerializer, UserNotificationSerializer

from posts.models import SavePost
from users.models import UserFCMToken, UserFollow, UserNotification

# new post
def send_to_reader_about_new_post(type, userObj, postObj):
    notiTemplateObj = NotiTemplate.objects.get(notitemp_type=type)

    allSendUserObj = User.objects.filter(username__in=Subquery(UserFollow.objects.values('uf_reading').filter(uf_reader=userObj.username))) #나를 따라오는 사람들한테 알려야함
    userFCMTokenObj = UserFCMToken.objects.filter(ufcm_user_id__in=allSendUserObj)
    getSerializerClass = UserFCMTokenSerializer(userFCMTokenObj, many=True)
    
    try:
        for odict in getSerializerClass.data:
            if odict['ufcm_token'] != None:

                userNotificationObj = UserNotification.objects.create(
                    un_token_id = UserFCMToken.objects.get(ufcm_token=odict['ufcm_token'], ufcm_device_id=odict['ufcm_device_id']),
                    un_type=notiTemplateObj,
                    un_title=userObj.first_name,
                    un_to=User.objects.get(username=odict['ufcm_user_id']['username']), #누구에게
                    un_from=userObj, # 누가
                    un_body=notiTemplateObj.notitemp_body,
                    un_etc=postObj
                )

                send_to_firebase_cloud_messaging(userObj.first_name,notiTemplateObj.notitemp_body,odict['ufcm_token'], userNotificationObj)
                            
    except Exception as e:
        print('out of for loop')
        print(e)

# postcomment를 적었을 때
def send_to_reader_about_new_comment(type, isMine, reqdata, userObj, postObj, pc_comment):
    notiTemplateObj = NotiTemplate.objects.get(notitemp_type=type)

    if isMine: # 내 글 : 리더, 글 구독하고 있던 사람
        allSendUserObj = User.objects.filter(username__in=Subquery(SavePost.objects.values('id').filter(b_id=postObj.b_id))) | User.objects.filter(username__in=Subquery(UserFollow.objects.values('uf_reading').filter(uf_reader=userObj.username)))
        userFCMTokenObj = UserFCMToken.objects.filter(ufcm_user_id__in=allSendUserObj)
        getSerializerClass = UserFCMTokenSerializer(userFCMTokenObj, many=True)
        
        try:
            for odict in getSerializerClass.data:
                if odict['ufcm_token'] != None:
                    userNotificationObj = UserNotification.objects.create(
                        un_token_id = UserFCMToken.objects.get(ufcm_token=odict['ufcm_token'], ufcm_device_id=odict['ufcm_device_id']),
                        un_type=notiTemplateObj,
                        un_title=userObj.first_name,
                        un_to=User.objects.get(username=odict['ufcm_user_id']['username']), #누구에게
                        un_from=userObj, # 누가
                        un_body=pc_comment,
                        un_etc=postObj
                    )

                    send_to_firebase_cloud_messaging(userObj.first_name,pc_comment,odict['ufcm_token'], userNotificationObj)
                                
        except Exception as e:
            print('out of for loop')
            print(e)

    elif isMine == False: # 누군가 내 글에 답글을 달았다...!!!
        postHostObj = User.objects.get(username=postObj.id)
        userFCMTokenObj = UserFCMToken.objects.filter(ufcm_user_id=postHostObj)
        getSerializerClass = UserFCMTokenSerializer(userFCMTokenObj, many=True)

        try:
            for odict in getSerializerClass.data:
                if odict['ufcm_token'] != None:
                    # print(odict['ufcm_token'])
                    # print(odict['ufcm_device_id'])
                    userNotificationObj = UserNotification.objects.create(
                        un_token_id = UserFCMToken.objects.get(ufcm_token=odict['ufcm_token'], ufcm_device_id=odict['ufcm_device_id']),
                        un_type=notiTemplateObj,
                        un_title=userObj.first_name,
                        un_to=User.objects.get(username=odict['ufcm_user_id']['username']),
                        un_from=userObj,
                        un_body=pc_comment,
                        un_etc=postObj
                    )

                    send_to_firebase_cloud_messaging(userObj.first_name,pc_comment,odict['ufcm_token'], userNotificationObj)
                                
        except Exception as e:
            print('out of for loop')
            print(e)

# postplace를 추가했을 때
def send_to_user_about_who_add_place(type, isMine, userObj, postObj):
    notiTemplateObj = NotiTemplate.objects.get(notitemp_type=type)

    if isMine: # 내 글 : 리더, 글 구독하고 있던 사람
        allSendUserObj = User.objects.filter(username__in=Subquery(SavePost.objects.values('id').filter(b_id=postObj.b_id))) | User.objects.filter(username__in=Subquery(UserFollow.objects.values('uf_reading').filter(uf_reader=userObj.username)))
        userFCMTokenObj = UserFCMToken.objects.filter(ufcm_user_id__in=allSendUserObj)
        getSerializerClass = UserFCMTokenSerializer(userFCMTokenObj, many=True)
        
        try:
            for odict in getSerializerClass.data:
                if odict['ufcm_token'] != None:
                    userNotificationObj = UserNotification.objects.create(
                        un_token_id = UserFCMToken.objects.get(ufcm_token=odict['ufcm_token'], ufcm_device_id=odict['ufcm_device_id']),
                        un_type=notiTemplateObj,
                        un_title=userObj.first_name,
                        un_to=User.objects.get(username=odict['ufcm_user_id']['username']), #누구에게
                        un_from=userObj, # 누가
                        un_body=notiTemplateObj.notitemp_body,
                        un_etc=postObj
                    )

                    send_to_firebase_cloud_messaging(userObj.first_name, notiTemplateObj.notitemp_body, odict['ufcm_token'], userNotificationObj)
                                
        except Exception as e:
            print('out of for loop')
            print(e)

    elif isMine == False: # 누군가 내 글에 답글을 달았다...!!!
        postHostObj = User.objects.get(username=postObj.id)
        userFCMTokenObj = UserFCMToken.objects.filter(ufcm_user_id=postHostObj)
        getSerializerClass = UserFCMTokenSerializer(userFCMTokenObj, many=True)

        try:
            for odict in getSerializerClass.data:
                if odict['ufcm_token'] != None:
                    userNotificationObj = UserNotification.objects.create(
                        un_token_id = UserFCMToken.objects.filter(ufcm_token=odict['ufcm_token'], ufcm_device_id=odict['ufcm_device_id']),
                        un_type=notiTemplateObj,
                        un_title=userObj.first_name,
                        un_to=User.objects.get(username=odict['ufcm_user_id']['username']),
                        un_from=userObj,
                        un_body=notiTemplateObj.notitemp_body,
                        un_etc=postObj
                    )

                    send_to_firebase_cloud_messaging(userObj.first_name,notiTemplateObj.notitemp_body,odict['ufcm_token'], userNotificationObj)
                                
        except Exception as e:
            print('out of for loop')
            print(e)

# image를 추가했을 때
def send_to_user_about_who_add_image(type, isMine, userObj, postObj):
    notiTemplateObj = NotiTemplate.objects.get(notitemp_type=type)

    if isMine: # 내 글 : 리더, 글 구독하고 있던 사람
        allSendUserObj = User.objects.filter(username__in=Subquery(SavePost.objects.values('id').filter(b_id=postObj.b_id))) | User.objects.filter(username__in=Subquery(UserFollow.objects.values('uf_reading').filter(uf_reader=userObj.username)))
        userFCMTokenObj = UserFCMToken.objects.filter(ufcm_user_id__in=allSendUserObj)
        getSerializerClass = UserFCMTokenSerializer(userFCMTokenObj, many=True)
        
        try:
            for odict in getSerializerClass.data:
                if odict['ufcm_token'] != None:
                    userNotificationObj = UserNotification.objects.create(
                        un_token_id = UserFCMToken.objects.get(ufcm_token=odict['ufcm_token'], ufcm_device_id=odict['ufcm_device_id']),
                        un_type=notiTemplateObj,
                        un_title=userObj.first_name,
                        un_to=User.objects.get(username=odict['ufcm_user_id']['username']), #누구에게
                        un_from=userObj, # 누가
                        un_body=notiTemplateObj.notitemp_body,
                        un_etc=postObj
                    )

                    send_to_firebase_cloud_messaging(userObj.first_name, notiTemplateObj.notitemp_body, odict['ufcm_token'], userNotificationObj)
                                
        except Exception as e:
            print('out of for loop')
            print(e)

    elif isMine == False: # 누군가 내 글에 답글을 달았다...!!!
        postHostObj = User.objects.get(username=postObj.id)
        userFCMTokenObj = UserFCMToken.objects.filter(ufcm_user_id=postHostObj)
        getSerializerClass = UserFCMTokenSerializer(userFCMTokenObj, many=True)

        try:
            for odict in getSerializerClass.data:
                if odict['ufcm_token'] != None:
                    userNotificationObj = UserNotification.objects.create(
                        un_token_id = UserFCMToken.objects.filter(ufcm_token=odict['ufcm_token'], ufcm_device_id=odict['ufcm_device_id']),
                        un_type=notiTemplateObj,
                        un_title=userObj.first_name,
                        un_to=User.objects.get(username=odict['ufcm_user_id']['username']),
                        un_from=userObj,
                        un_body=notiTemplateObj.notitemp_body,
                        un_etc=postObj
                    )

                    send_to_firebase_cloud_messaging(userObj.first_name,notiTemplateObj.notitemp_body,odict['ufcm_token'], userNotificationObj)
                                
        except Exception as e:
            print('out of for loop')
            print(e)
          
# 누군가 내 글을 구독했을 때
def send_to_user_about_who_saved_post(type, userObj, postObj):
    notiTemplateObj = NotiTemplate.objects.get(notitemp_type=type)

    sendUserObj = User.objects.filter(username=postObj.id)
    userFCMTokenObj = UserFCMToken.objects.filter(ufcm_user_id__in=sendUserObj)

    getSerializerClass = UserFCMTokenSerializer(userFCMTokenObj, many=True)
    
    try:
        for odict in getSerializerClass.data:
            if odict['ufcm_token'] != None:

                un_from = User.objects.get(username=odict['ufcm_user_id']['username'])
                ufcm = UserFCMToken.objects.get(ufcm_token=odict['ufcm_token'], ufcm_device_id=odict['ufcm_device_id'])

                c = UserNotification.objects.filter(un_token_id=ufcm, un_type=notiTemplateObj, un_from=un_from, un_to=userObj, un_send_date__range=[datetime.now()-timedelta(minutes=1), datetime.now()]).count()
                if c == 0:
                    userNotificationObj = UserNotification.objects.create(
                        un_token_id = UserFCMToken.objects.get(ufcm_token=odict['ufcm_token'], ufcm_device_id=odict['ufcm_device_id']),
                        un_type=notiTemplateObj,
                        un_title=un_from.first_name,
                        un_to=userObj, #누구에게
                        un_from=un_from, # 누가
                        un_body=notiTemplateObj.notitemp_body,
                        un_etc=postObj
                    )

                    send_to_firebase_cloud_messaging(userObj.first_name, notiTemplateObj.notitemp_body, odict['ufcm_token'], userNotificationObj)
                            
    except Exception as e:
        print('out of for loop')
        print(e)

# 누군가 나를 팔로우 했을 때
def send_to_user_about_who_followed_user(type, fromObj, toObj):
    notiTemplateObj = NotiTemplate.objects.get(notitemp_type=type)

    sendUserObj = User.objects.filter(username=toObj.username)
    userFCMTokenObj = UserFCMToken.objects.filter(ufcm_user_id__in=sendUserObj)

    getSerializerClass = UserFCMTokenSerializer(userFCMTokenObj, many=True)
    
    try:
        for odict in getSerializerClass.data:
            if odict['ufcm_token'] != None:
                ufcm = UserFCMToken.objects.get(ufcm_token=odict['ufcm_token'], ufcm_device_id=odict['ufcm_device_id'])
                
                # 1분 동안 이미 보내진 거 잇느으면 안 보냄
                c = UserNotification.objects.filter(un_token_id=ufcm, un_type=notiTemplateObj, un_from=fromObj, un_to=toObj, un_send_date__range=[datetime.now()-timedelta(minutes=1), datetime.now()]).count()

                if c == 0:
                    # un_from = User.objects.get(username=odict['ufcm_user_id']['username'])

                    userNotificationObj = UserNotification.objects.create(
                        un_token_id = ufcm,
                        un_type=notiTemplateObj,
                        un_title=fromObj.first_name,
                        un_to=toObj, #누구에게
                        un_from=fromObj, # 누가
                        un_body=notiTemplateObj.notitemp_body
                    )

                    send_to_firebase_cloud_messaging(fromObj.first_name, notiTemplateObj.notitemp_body, odict['ufcm_token'], userNotificationObj)
                            
    except Exception as e:
        print('out of for loop')
        print(e)



def send_to_firebase_cloud_messaging(title, body, token, obj): #  token, device_id
    # This registration token comes from the client FCM SDKs.
    registration_token = token
    getSerializerClass = UserNotificationSerializer(obj)
    # print(getSerializerClass.data)
    # See documentation on defining a message payload.
    message = messaging.Message(

        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=registration_token,
        data={'param': json.dumps(getSerializerClass.data)},
    )

    try:
        response = messaging.send(message)

        print(f"Successfully sent message: {response}")

        obj.un_is_sended = True
        obj.save()

    except Exception as e:
        print("예외가 발생했습니다.", e)