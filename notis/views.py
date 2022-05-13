from django.shortcuts import render
from firebase_admin import messaging
from .models  import *

def send_to_reader_about_new_comment(type, isMine, reqdata, userObj, postObj):
    if type == 'pc_comment_create':
        print('1')

def send_to_firebase_cloud_messaging(title, body, token): #  token, device_id
    # This registration token comes from the client FCM SDKs.
    registration_token = token

    # See documentation on defining a message payload.
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=registration_token,
    )

    try:
        response = messaging.send(message)
        print(f"Successfully sent message: {response}")
    except Exception as e:
        print("예외가 발생했습니다.", e)

    # Response is a message ID string.
    print('Successfully sent message:', response)