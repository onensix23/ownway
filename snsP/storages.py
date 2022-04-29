import uuid
from datetime import datetime
from snsP.my_settings import *
from boto3 import *
from PIL import Image, ExifTags, ImageOps   # 이미지 리사이징에 필요한 Pillow
from io  import BytesIO # Pillow로 리사이징한 이미지를 다시 Bytes화
from storages.backends.s3boto3 import S3Boto3Storage

__all__ = (
    'S3StaticStorage',
    'S3DefaultStorage',
)


# 정적 파일용
class S3StaticStorage(S3Boto3Storage):
    default_acl = 'public-read'
    location = 'static'


# 미디어 파일용
class S3DefaultStorage(S3Boto3Storage):
    default_acl = 'private'
    location = 'media'


class FileUpload:
    def __init__(self, client):
        self.client = client

    def upload(self, file):
        return self.client.upload(file)

    def delete(self, file):
        return self.client.delete(file)


class MyS3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        boto3_s3 = client(
            's3',
            aws_access_key_id     = access_key,
            aws_secret_access_key = secret_key
        )
        self.s3_client   = boto3_s3
        self.bucket_name = bucket_name

    def upload(self, file):
        try: 
            now_date = datetime.now().strftime('%Y%m%d')
            file_id = 'media/images/'+now_date+'/'+str(uuid.uuid4())
            extra_args = { 'ContentType' : file.content_type }

            im = Image.open(file)
            im = ImageOps.exif_transpose(im)
            # im = im.resize((1920, 1920))

            # for orientation in ExifTags.TAGS.keys():
            #     if ExifTags.TAGS[orientation]=='Orientation':
            #         break

            #     temp = im.getexif()[0x0112]
            #     if temp == 3:
            #         im=im.rotate(180, expand=True)
            #     elif temp == 6:
            #         im=im.rotate(270, expand=True)
            #     elif temp == 8:
                    # im=im.rotate(90, expand=True)
                    
            buffer = BytesIO()
            im.save(buffer, "JPEG")
            buffer.seek(0)

            self.s3_client.upload_fileobj(
                    buffer, #file,
                    self.bucket_name,
                    file_id,
                    ExtraArgs = extra_args
                )
            return f'https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_id}'
        except Exception as e:
            print(e)
            return None

    
    def delete(self, filename):
        key = filename.split('https://ownway-bucket.s3.ap-northeast-2.amazonaws.com/')[1]

        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            return 1
        except:
            return 0
       

        # self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)


# MyS3Client instance
s3_client = MyS3Client(AWS_S3_ACCESS_KEY_ID, AWS_S3_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)