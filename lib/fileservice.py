# import boto
import boto3
# from boto.s3.key import Key

AWS_ACCESS_KEY_ID = 'AKIAJBP2UJSYCRTPEJ2Q'
AWS_SECRET_ACCESS_KEY = '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'

def uploadFile(fileName):
    s3 = boto3.resource('s3')

    data = open(fileName, 'rb')
    s3.Bucket('pi-spy').put_object(ACL='public-read', ContentType='image/jpeg', Key='images/' + fileName, Body=data)


    # client = boto3.client(
    #     's3',
    #     aws_access_key_id=ACCESS_KEY,
    #     aws_secret_access_key=SECRET_KEY,
    #     aws_session_token=SESSION_TOKEN,
    # )
    #
    # data = open(fileName, 'rb')
    #
    # client.Bucket('pi-spy').put_object(Key='still.jpg', Body=data)

    # s3 = boto3.resource('s3')
    # data = open(fileName, 'rb')
    # s3.Bucket('pi-spy').put_object(Key='still.jpg', Body=data)


    # conn = boto3.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    # bucket = conn.get_bucket('pi-spy', validate=True)
    #
    # key = bucket.new_key('images/' + fileName)
    # key.set_contents_from_filename(fileName)
    #
    # # k = Key(bucket)
    # # k.key = key
    #
    # s3 = boto3.resource('s3')
    # data = open(fileName, 'rb')
    # s3.Bucket('pi-spy').put_object(Key='still.jpg', Body=data)
