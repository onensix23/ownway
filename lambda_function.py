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


    def insertUnnest(self,param):
        query = """insert into public.users_usernotification (un_token_id, un_type, un_title, un_to, un_from, un_body, un_is_sended, un_etc) 
        select unnest(%(un_token_id)s), unnest(%(un_type)s), unnest(%(un_title)s) 
            ,unnest(%(un_to)s) ,unnest(%(un_from)s)
            ,unnest(%(un_body)s), unnest(%(un_is_sended)s), unnest(%(un_etc)s) """

        try:
            print('----1-----')
            with self.db as conn:
                print('----2-----')
                with conn.cursor() as curs:
                    print('----3-----')
                    if len(param['un_token_id']) > 0 :
                        print('----4-----')
                        curs.execute(query, param)

                        conn.commit()

                    curs.close()
        
        except Exception as e :
            print(e)
            result = (" update DB err",e)

    def updateDB(self,query):
        sql = query
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" update DB err",e)

    def readDB(self,schema,table,colum):
        sql = " SELECT {colum} from {schema}.{table}".format(colum=colum,schema=schema,table=table)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e :
            result = (" read DB err",e)
        
        return result

    def updateDB(self,schema,table,colum,value,condition):
        sql = "UPDATE {schema}.{table} SET {colum}='{value}' WHERE {colum}='{condition}' ".format(schema=schema
        , table=table , colum=colum ,value=value,condition=condition )
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" update DB err",e)


    def send_to_firebase_cloud_messaging(self, title, body, token, token_id, etc): #  token, device_id
        # print(title, body, token, token_id, etc)
        firebase_admin.get_app()
        
        # This registration token comes from the client FCM SDKs.
        print('send_to_firebase_cloud_messaging')
        sendData = {
            'un_title' : title,
            'un_body' : body,
            'un_token' : token,
            'un_token_id' : token_id,
            'un_etc' : etc
        }
        res = {'res' : False}

        registration_token = token
        registration_token = 'dUo95LOfakWMlBLmapsW3C:APA91bGyHYy5XuzJNejPJkLxije4DqXdwI6pM-wTP4I6QOacHlkQH-ThXJbrai70cZdOvDd7YenVQ30hV-VPjSHbRFyOSwJbPJi9SB43AYjnIotjdvanMIWMOwaSKTjrJYo7tOp4bzx8'

        try:
            print('hi')
            # See documentation on defining a message payload.
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                token=registration_token,
                data={'param': json.dumps(sendData)},
            )

            print("lets go")
            response = messaging.send(message)
            print(f"Successfully sent message: {response}")
            res['res'] = True
            
            print(res)

            return res
        except Exception as e:
            print(e)

            return res

            
    

    def send_to_reader_about_new_comment(self, type, username, b_id, pc_comment):
        un_token =[]
        un_token_id = []
        un_type = []
        un_title = []
        un_to = []
        un_from = []
        un_body = []
        un_is_sended = []
        un_etc = []

        try:
            user_data = self.readQuery("select username, first_name from auth_user where username = '{0}'".format(username),'one')
            postObj_id = self.readQuery("select id from posts_posts where b_id='{0}'".format(b_id), 'one')

            if username == postObj_id[0]: #mine

                allSendUserObj = self.readQuery("""select * 
                                                from users_userfcmtoken
                                                where ufcm_user_id in (
                                                select id from posts_savepost where b_id = '{0}' and sp_is_noti=true
                                                )""".format(b_id), 'all')
                
                for odict in allSendUserObj:
                    if odict['ufcm_token'] != None and odict['ufcm_user_id'] != username:

                        sql = "select ufcm_id from users_userfcmtoken where ufcm_token = '{0}' and ufcm_device_id = '{1}'".format(odict['ufcm_token'], odict['ufcm_device_id'])
                        ufcm_token_data = self.readQuery(sql, 'one')

                        un_token_id.append(ufcm_token_data[0])
                        un_type.append(type)
                        un_title.append(user_data[1])
                        un_to.append(username)
                        un_from.append(odict['ufcm_user_id'])
                        un_body.append(pc_comment)
                        un_etc.append(int(b_id))

                        ans = self.send_to_firebase_cloud_messaging(user_data[1],pc_comment, odict['ufcm_token'],ufcm_token_data[0], int(b_id))

                        if ans['res'] == True :
                            un_is_sended.append(True)
                        else:
                            un_is_sended.append(False)

            else: #others
                savepostObj = self.readQuery("""select sp_is_noti from posts_savepost where id = '{0}' and b_id = {1}""".format(postObj_id[0], b_id), 'one')
                if((savepostObj != None and savepostObj[0] == True) or (savepostObj==None)):
                    allSendUserObj1 = self.readQuery("""select * 
                                                from users_userfcmtoken
                                                where ufcm_user_id = '{0}'""".format(postObj_id[0]), 'all')

                    for odict in allSendUserObj1:
                        if odict['ufcm_token'] != None and odict['ufcm_user_id'] != username:
                            sql = "select ufcm_id from users_userfcmtoken where ufcm_token = '{0}' and ufcm_device_id = '{1}'".format(odict['ufcm_token'], odict['ufcm_device_id'])
                            ufcm_token_data = self.readQuery(sql, 'one')

                            un_token_id.append(ufcm_token_data[0])
                            un_token.append(odict['ufcm_token'])
                            un_type.append(type)
                            un_title.append(user_data[1])
                            un_to.append(username)
                            un_from.append(odict['ufcm_user_id'])
                            un_body.append(pc_comment)
                            un_etc.append(int(b_id))

                            ans = self.send_to_firebase_cloud_messaging(user_data[1],pc_comment, odict['ufcm_token'],ufcm_token_data[0], int(b_id))

                            if ans['res'] == True :
                                un_is_sended.append(True)
                            else:
                                un_is_sended.append(False)
                            
            param = {'un_token_id': un_token_id, 'un_type': un_type, 'un_title': un_title
            , 'un_to': un_to, 'un_from': un_from, 'un_body': un_body, 'un_is_sended': un_is_sended, 'un_etc': un_etc}

            self.insertUnnest(param)
                                
        except Exception as e:
            print('out of for loop')
            print(e)


def lambda_handler(event):
    # {'pc_id': '634', 'pc_comment': 'kk', 'b_id': '115', 'id': '1142995766470027', 'type' ,'pc_c'}
    print(event)

    cred = credentials.Certificate('./ownway-firebase-adminsdk-servicekey.json')            
    default_app = firebase_admin.initialize_app(cred)

    try:
        db = CRUD()
        #Namespace(arg1='709', arg2='Fw', arg3='0114', arg4='101960524939177545327', arg5='pc_c', arg6='false')
        if event.arg5 == 'pc_c':
            # type, username, b_id, pc_comment
            db.send_to_reader_about_new_comment(event.arg5, event.arg4, event.arg3, event.arg2)
        elif event.arg5 == 'pp_c':
            print(db.readDB(schema='public',table='auth_user',colum='*'))
        elif event.arg5 == 'im_c':
            print(db.readDB(schema='public',table='auth_user',colum='*'))
        elif event.arg5 == 'sp_c':
            print(db.readDB(schema='public',table='auth_user',colum='*'))
        elif event.arg5 == 'fu_c':
            print(db.readDB(schema='public',table='auth_user',colum='*'))
        # elif event.arg6 ==  'p_c':
        #     db.send_to_reader_about_new_post(event.arg6, event['id'], event['b_id'])
            # print(db.readDB(schema='public',table='auth_user',colum='*'))
    except Exception as e:
        print('error1')
        print(e)

    return {
        'statusCode': 200,
        'body': '234',
        'res':event
    }

lambda_handler(args)