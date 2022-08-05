import psycopg2, pathlib, json
import psycopg2.extras
import requests

import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials

from datetime import timedelta
from snsP import my_settings
import argparse

parser = argparse.ArgumentParser(description='이 프로그램의 설명(그 외 기타등등 아무거나)')    # 2. parser를 만든다.

# 3. parser.add_argument로 받아들일 인수를 추가해나간다.
parser.add_argument('arg1',)    # 필요한 인수를 추가
parser.add_argument('arg2',)
parser.add_argument('arg3',)    # 필요한 인수를 추가
parser.add_argument('arg4',)
parser.add_argument('arg5',)    # 필요한 인수를 추가
parser.add_argument('arg6',)

args = parser.parse_args()

class Databases():
    def __init__(self):
        self.db = psycopg2.connect(host=my_settings.DATABASES['default']['HOST'], 
        dbname=my_settings.DATABASES['default']['NAME'],user=my_settings.DATABASES['default']['USER'],
        password=my_settings.DATABASES['default']['PASSWORD'],port=my_settings.DATABASES['default']['PORT'])
        self.db.autocommit=True
        self.cursor = self.db.cursor(cursor_factory = psycopg2.extras.DictCursor)

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self,query,args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.cursor.commit()


class CRUD(Databases):
    def readQuery(self,query, fetchtype):
        sql = query
        try:
            with self.db as conn:
                with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as curs: 
                    curs.execute(sql)
                    if fetchtype == 'all':
                        result = curs.fetchall()
                    elif fetchtype == 'one':
                        result = curs.fetchone()

                    curs.close()

        except Exception as e :
            print(e)
            result = (" read DB err",e)

        return result

    def updateQuery(self,query):
        sql = query
        try:
            with self.db as conn:
                with conn.cursor() as curs: 
                    curs.execute(sql)
                    conn.commit()

                    curs.close()

        except Exception as e :
            result = (" update DB err",e)

        return result

    def insertQuery(self,query,param):
        try:
            with self.db as conn:
                with conn.cursor(auto_commit=True) as curs: 
                    curs.execute(query, param)
                    conn.commit()

                    curs.close()
        
        except Exception as e :
            result = (" update DB err",e)
        
        return result


    def insertUnnest(self,param, t):
        query = """insert into public.users_usernotification (un_token_id, un_type, un_title, un_to, un_from, un_body, un_is_sended, un_etc) 
        select unnest(%(un_token_id)s), unnest(%(un_type)s), unnest(%(un_title)s) 
            ,unnest(%(un_to)s) ,unnest(%(un_from)s),unnest(%(un_body)s), 
            unnest(%(un_is_sended)s), unnest(%(un_etc)s)"""

        
        query2 = """insert into public.users_usernotification (un_token_id, un_type, un_title, un_to, un_from, un_body, un_is_sended) 
        select unnest(%(un_token_id)s), unnest(%(un_type)s), unnest(%(un_title)s) 
            ,unnest(%(un_to)s) ,unnest(%(un_from)s),unnest(%(un_body)s), 
            unnest(%(un_is_sended)s)"""
            
        query3 = """insert into public.users_usernotification (un_token_id, un_type, un_title, un_to, un_from, un_body, un_is_sended, un_etc, un_detail_etc) 
        select unnest(%(un_token_id)s), unnest(%(un_type)s), unnest(%(un_title)s) 
            ,unnest(%(un_to)s) ,unnest(%(un_from)s),unnest(%(un_body)s), 
            unnest(%(un_is_sended)s), unnest(%(un_etc)s) , unnest(%(un_detail_etc)s)"""

        try:
            with self.db as conn:
                with conn.cursor() as curs:
                    if len(param['un_token_id']) > 0 :
                        if t == 'fu_c':
                            curs.execute(query2, param)
                        elif t == 'pc_c':
                            curs.execute(query3, param)
                        else:
                            curs.execute(query, param)

                        conn.commit()

                    curs.close()
        
        except Exception as e :
            print(e)

    def send_to_firebase_cloud_messaging(self, type, title, body, token, token_id, etc): #  token, device_id
        # print(title, body, token, token_id, etc)
        firebase_admin.get_app()
        
        # This registration token comes from the client FCM SDKs.
        print('send_to_firebase_cloud_messaging')

        sendData = {
            'un_title' : title,
            'un_body' : body,
            'un_token' : token,
            'un_token_id' : token_id,
            'un_type': type,
            'un_etc' : etc
        }
        res = {'res' : False}

        registration_token = token
        
        try:
            # See documentation on defining a message payload.
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                android=messaging.AndroidConfig( 
                    priority='high', 
                    notification=messaging.AndroidNotification( sound='default' ), 
                ), 
                apns=messaging.APNSConfig( 
                    payload=messaging.APNSPayload( 
                        aps=messaging.Aps( sound='default' ), 
                    ), 
                ), 
                token=registration_token,
                data={'param': json.dumps(sendData)},
            )

            response = messaging.send(message)
            print(f"Successfully sent message: {response}")
            res['res'] = True
            
            return res
        except Exception as e:
            print(e)

            return res    
    

    def send_to_reader_about_new_comment(self, type, username, b_id, pc_comment, pc_id):
        un_token_id = []
        un_type = []
        un_title = []
        un_to = []
        un_from = []
        un_body = []
        un_is_sended = []
        un_etc = []
        un_detail_etc = []

        try:
            user_data = self.readQuery("select username, first_name from auth_user where username = '{0}'".format(username),'one')
            postObj_id = self.readQuery("select id from posts_posts where b_id='{0}'".format(b_id), 'one')
                    
            if username == postObj_id[0]: #mine
                
                query_pc_c = """select * 
                            from users_userfcmtoken
                            where ufcm_user_id in (
                                select id from posts_savepost where b_id = '{0}' and sp_is_noti=true
                            ) and ufcm_pc_c = true
                            union
                            select * 
                            from users_userfcmtoken
                            where ufcm_user_id in (
                                select unc_user_id from users_usernoticount where unc_b_id = '{1}'
                            ) and ufcm_pc_c = true""".format(b_id, b_id)
                query_pc_u = """select * 
                            from users_userfcmtoken
                            where ufcm_user_id in (
                                select id from posts_savepost where b_id = '{0}' and sp_is_noti=true
                            ) and ufcm_pc_u = true
                            union
                            select * 
                            from users_userfcmtoken
                            where ufcm_user_id in (
                                select unc_user_id from users_usernoticount where unc_b_id = '{1}'
                            ) and ufcm_pc_u = true""".format(b_id, b_id)
                            
                allSendUserObj = self.readQuery((query_pc_c if type == 'pc_c' else query_pc_u), 'all')

                for odict in allSendUserObj:
                    if odict['ufcm_token'] != None and odict['ufcm_user_id'] != username:

                        sql = "select ufcm_id from users_userfcmtoken where ufcm_token = '{0}' and ufcm_device_id = '{1}'".format(odict['ufcm_token'], odict['ufcm_device_id'])
                        ufcm_token_data = self.readQuery(sql, 'one')

                        un_token_id.append(ufcm_token_data[0])
                        un_type.append(type)
                        un_title.append(user_data[1])
                        un_to.append(odict['ufcm_user_id'])
                        un_from.append(username)
                        un_body.append(pc_comment)
                        un_etc.append(int(b_id))
                        un_detail_etc.append(int(pc_id))

                        ans = self.send_to_firebase_cloud_messaging(type, user_data[1],pc_comment, odict['ufcm_token'],ufcm_token_data[0], int(b_id))

                        if ans['res'] == True :
                            un_is_sended.append(True)
                        else:
                            un_is_sended.append(False)

            else: #others
                savepostObj = self.readQuery("""select sp_is_noti from posts_savepost where id = '{0}' and b_id = {1}""".format(postObj_id[0], b_id), 'one')
                
                if((savepostObj != None and savepostObj[0] == True) or (savepostObj==None)):
                    
                    query_pc_c = """select * 
                                    from users_userfcmtoken
                                    where ufcm_user_id in (
                                        select id from posts_savepost where b_id = {0} and sp_is_noti=true
                                    ) and ufcm_pc_c = true and ufcm_token is not null
                                    union
                                    select * 
                                    from users_userfcmtoken
                                    where ufcm_user_id in (
                                        select unc_user_id from users_usernoticount where unc_b_id = {1}
                                    ) and ufcm_pc_c = true and ufcm_token is not null
                                    union
                                    select * 
                                    from users_userfcmtoken
                                    where ufcm_user_id ='{2}'
                                    and ufcm_pc_c = true and ufcm_token is not null""".format(postObj_id[0],postObj_id[0], username)
                                    
                    query_pc_u = """select * 
                                    from users_userfcmtoken
                                    where ufcm_user_id in (
                                        select id from posts_savepost where b_id = {0} and sp_is_noti=true
                                    ) and ufcm_pc_u = true and ufcm_token is not null
                                    union
                                    select * 
                                    from users_userfcmtoken
                                    where ufcm_user_id in (
                                        select unc_user_id from users_usernoticount where unc_b_id = {1}
                                    ) and ufcm_pc_u = true and ufcm_token is not null
                                    union
                                    select * 
                                    from users_userfcmtoken
                                    where ufcm_user_id ='{2}'
                                    and ufcm_pc_u = true and ufcm_token is not null""".format(postObj_id[0],postObj_id[0], username)
                                    
                    allSendUserObj1 = self.readQuery((query_pc_c if type == 'pc_c' else query_pc_u), 'all')

                    for odict in allSendUserObj1:
                        if odict['ufcm_token'] != None and odict['ufcm_user_id'] != username:
                            sql = "select ufcm_id from users_userfcmtoken where ufcm_token = '{0}' and ufcm_device_id = '{1}'".format(odict['ufcm_token'], odict['ufcm_device_id'])
                            ufcm_token_data = self.readQuery(sql, 'one')

                            un_token_id.append(ufcm_token_data[0])
                            un_type.append(type)
                            un_title.append(user_data[1])
                            un_to.append(odict['ufcm_user_id'])
                            un_from.append(username)
                            un_body.append(pc_comment)
                            un_etc.append(int(b_id))
                            un_detail_etc.append(int(pc_id))

                            ans = self.send_to_firebase_cloud_messaging(type,user_data[1],pc_comment, odict['ufcm_token'],ufcm_token_data[0], int(b_id))

                            if ans['res'] == True :
                                un_is_sended.append(True)
                            else:
                                un_is_sended.append(False)
                            
            param = {'un_token_id': un_token_id, 'un_type': un_type, 'un_title': un_title
            , 'un_to': un_to, 'un_from': un_from, 'un_body': un_body, 'un_is_sended': un_is_sended, 'un_etc': un_etc, 'un_detail_etc': un_detail_etc}

            
            self.insertUnnest(param, type)
                                
        except Exception as e:
            print('out of for loop')
            print(e)

    # postplace를 추가했을 때
    # pp_c user_id b_id
    def send_to_user_about_who_add_place(self, type, username, b_id):

        un_token =[]
        un_token_id = []
        un_type = []
        un_title = []
        un_to = []
        un_from = []
        un_body = []
        un_is_sended = []
        un_etc = []

        user_data = self.readQuery("select username, first_name from auth_user where username = '{0}'".format(username),'one')
        postObj_id = self.readQuery("select id from posts_posts where b_id='{0}'".format(b_id), 'one')
        
        notiTemplateObj = self.readQuery("select notitemp_body from notis_notitemplate where notitemp_type = '{0}'".format(type), 'one')
        
        if username == postObj_id[0]: #mine: # 내 글 : 리더, 글 구독하고 있던 사람
            try:
                allSendUserObj = self.readQuery("""select * 
                                                from users_userfcmtoken
                                                where ufcm_user_id in (
                                                select id from posts_savepost where b_id = '{0}' and sp_is_noti=true
                                                ) and ufcm_pp_c = true""".format(b_id), 'all')
                
                for odict in allSendUserObj:
                    if odict['ufcm_token'] != None and odict['ufcm_user_id'] != username:

                        sql = "select ufcm_id from users_userfcmtoken where ufcm_token = '{0}' and ufcm_device_id = '{1}'".format(odict['ufcm_token'], odict['ufcm_device_id'])
                        ufcm_token_data = self.readQuery(sql, 'one')

                        un_token_id.append(ufcm_token_data[0])
                        un_type.append(type)
                        un_title.append(user_data[1])
                        un_to.append(odict['ufcm_user_id'])
                        un_from.append(username)
                        un_body.append(notiTemplateObj[0])
                        un_etc.append(int(b_id))

                        ans = self.send_to_firebase_cloud_messaging(type,user_data[1],notiTemplateObj[0], odict['ufcm_token'],ufcm_token_data[0], int(b_id))

                        if ans['res'] == True :
                            un_is_sended.append(True)
                        else:
                            un_is_sended.append(False)
                
                param = {'un_token_id': un_token_id, 'un_type': un_type, 'un_title': un_title
                , 'un_to': un_to, 'un_from': un_from, 'un_body': un_body, 'un_is_sended': un_is_sended, 'un_etc': un_etc}

                self.insertUnnest(param, type)
                            
            except Exception as e:
                print('out of for loop')
                print(e)

    # image를 추가했을 때
    def send_to_user_about_who_add_image(self, type, username, b_id):

        un_token_id = []
        un_type = []
        un_title = []
        un_to = []
        un_from = []
        un_body = []
        un_is_sended = []
        un_etc = []

        user_data = self.readQuery("select username, first_name from auth_user where username = '{0}'".format(username),'one')
        postObj_id = self.readQuery("select id from posts_posts where b_id='{0}'".format(b_id), 'one')
        
        notiTemplateObj = self.readQuery("select notitemp_body from notis_notitemplate where notitemp_type = '{0}'".format(type), 'one')
        
        if username == postObj_id[0]: #mine: # 내 글 : 리더, 글 구독하고 있던 사람
            try:
                allSendUserObj = self.readQuery("""select * 
                                                from users_userfcmtoken
                                                where ufcm_user_id in (
                                                select id from posts_savepost where b_id = '{0}' and sp_is_noti=true
                                                ) and ufcm_im_c = true""".format(b_id), 'all')
                
                for odict in allSendUserObj:
                    if odict['ufcm_token'] != None and odict['ufcm_user_id'] != username:

                        sql = "select ufcm_id from users_userfcmtoken where ufcm_token = '{0}' and ufcm_device_id = '{1}'".format(odict['ufcm_token'], odict['ufcm_device_id'])
                        ufcm_token_data = self.readQuery(sql, 'one')

                        un_token_id.append(ufcm_token_data[0])
                        un_type.append(type)
                        un_title.append(user_data[1])
                        un_to.append(odict['ufcm_user_id'])
                        un_from.append(username)
                        un_body.append(notiTemplateObj[0])
                        un_etc.append(int(b_id))

                        ans = self.send_to_firebase_cloud_messaging(type,user_data[1],notiTemplateObj[0], odict['ufcm_token'],ufcm_token_data[0], int(b_id))

                        if ans['res'] == True :
                            un_is_sended.append(True)
                        else:
                            un_is_sended.append(False)
                
                param = {'un_token_id': un_token_id, 'un_type': un_type, 'un_title': un_title
                , 'un_to': un_to, 'un_from': un_from, 'un_body': un_body, 'un_is_sended': un_is_sended, 'un_etc': un_etc}

                
                self.insertUnnest(param, type)
                            
            except Exception as e:
                print('out of for loop')
                print(e)
          
# 누군가 내 글을 구독했을 때
    def send_to_user_about_who_saved_post(self, type, username, p_username, b_id):
        
        # username 이  p_username 따르기 시작
        un_token_id = []
        un_type = []
        un_title = []
        un_to = []
        un_from = []
        un_body = []
        un_is_sended = []
        un_etc = []

        user_data = self.readQuery("select username, first_name from auth_user where username = '{0}'".format(username),'one')
        
        notiTemplateObj = self.readQuery("select notitemp_body from notis_notitemplate where notitemp_type = '{0}'".format(type), 'one')

        try:
            allSendUserObj = self.readQuery("""select * from users_userfcmtoken 
                                                where ufcm_user_id = '{0}' and ufcm_sp_c = true""".format(p_username), 'all')
            
            for odict in allSendUserObj:
                if odict['ufcm_token'] != None and odict['ufcm_user_id'] != username:

                    sql = "select ufcm_id from users_userfcmtoken where ufcm_token = '{0}' and ufcm_device_id = '{1}'".format(odict['ufcm_token'], odict['ufcm_device_id'])
                    ufcm_token_data = self.readQuery(sql, 'one')

                    sql1 = """select count(*) from users_usernotification where
                                un_token_id = '{0}' and un_type = '{1}' 
                                and un_from = '{2}' and un_to = '{3}' 
                                and  un_send_date between now() - interval '1 minute' and now()""".format(ufcm_token_data[0],type, username, p_username)
                    c = self.readQuery(sql1, 'one')
                    
                    if c[0] == 0:

                        un_token_id.append(odict['ufcm_id'])
                        un_type.append(type)
                        un_title.append(user_data[1])
                        un_to.append(odict['ufcm_user_id'])
                        un_from.append(username)
                        un_body.append(notiTemplateObj[0])
                        un_etc.append(int(b_id))

                        ans = self.send_to_firebase_cloud_messaging(type,user_data[1],notiTemplateObj[0], odict['ufcm_token'],ufcm_token_data[0], None)

                        if ans['res'] == True :
                            un_is_sended.append(True)
                        else:
                            un_is_sended.append(False)

            param = {'un_token_id': un_token_id, 'un_type': un_type, 'un_title': un_title
            , 'un_to': un_to, 'un_from': un_from, 'un_body': un_body, 'un_is_sended': un_is_sended, 'un_etc': un_etc}
            
            self.insertUnnest(param, type)
                        
        except Exception as e:
            print('out of for loop')
            print(e)
        

    # 누군가 나를 팔로우 했을 때
    def send_to_user_about_who_followed_user(self, type, fromuser, touser):

        un_token_id = []
        un_type = []
        un_title = []
        un_to = []
        un_from = []
        un_body = []
        un_is_sended = []
        un_etc = []

        user_data = self.readQuery("select username, first_name from auth_user where username = '{0}'".format(fromuser),'one')
        notiTemplateObj = self.readQuery("select notitemp_body from notis_notitemplate where notitemp_type = '{0}'".format(type), 'one')

        try:
            allSendUserObj = self.readQuery("""select * from users_userfcmtoken 
                                                where ufcm_user_id = '{0}' and ufcm_fu_c = true""".format(touser), 'all')
            
            for odict in allSendUserObj:
                if odict['ufcm_token'] != None and odict['ufcm_user_id'] != fromuser:

                    sql = "select ufcm_id from users_userfcmtoken where ufcm_token = '{0}' and ufcm_device_id = '{1}'".format(odict['ufcm_token'], odict['ufcm_device_id'])
                    ufcm_token_data = self.readQuery(sql, 'one')

                    sql1 = """select count(*) from users_usernotification where
                                un_token_id = '{0}' and un_type = '{1}' 
                                and un_from = '{2}' and un_to = '{3}' 
                                and  un_send_date between now() - interval '1 minute' and now()""".format(ufcm_token_data[0],type, fromuser, touser)
                    c = self.readQuery(sql1, 'one')
                    
                    if c[0] == 0:
                        un_token_id.append(odict['ufcm_id'])
                        un_type.append(type)
                        un_title.append(user_data[1])
                        un_to.append(odict['ufcm_user_id'])
                        un_from.append(fromuser)
                        un_body.append(notiTemplateObj[0])
                        un_etc.append(None)

                        ans = self.send_to_firebase_cloud_messaging(type,user_data[1], notiTemplateObj[0], odict['ufcm_token'],ufcm_token_data[0], None)

                        if ans['res'] == True :
                            un_is_sended.append(True)
                        else:
                            un_is_sended.append(False)

            param = {'un_token_id': un_token_id, 'un_type': un_type, 'un_title': un_title
            , 'un_to': un_to, 'un_from': un_from, 'un_body': un_body, 'un_is_sended': un_is_sended, 'un_etc': un_etc}
            
            self.insertUnnest(param, type)

        except Exception as e:
            print('out of for loop')
            print(e)



def lambda_handler(event):
    cred = credentials.Certificate('./ownway-firebase-adminsdk-servicekey.json')            
    default_app = firebase_admin.initialize_app(cred)

    try:
        db = CRUD()

        if event.arg5 == 'pc_c' or event.arg5 == 'pc_u':
            db.send_to_reader_about_new_comment(event.arg5, event.arg4, event.arg3, event.arg2, event.arg1)
        elif event.arg5 == 'pp_c':
            db.send_to_user_about_who_add_place(event.arg5,event.arg4, event.arg3)
        elif event.arg5 == 'im_c':
            db.send_to_user_about_who_add_image(event.arg5,event.arg4, event.arg3)
        elif event.arg5 == 'sp_c':
            # type, 따르는 사람 , 따라가는 사람
            db.send_to_user_about_who_saved_post(event.arg5,event.arg4, event.arg3, event.arg2)
        elif event.arg5 == 'fu_c':
            # type, 누가, 누구를
            db.send_to_user_about_who_followed_user(event.arg5,event.arg4, event.arg3)
    except Exception as e:
        print('error1')
        print(e)

lambda_handler(args)