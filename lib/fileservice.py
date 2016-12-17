# import boto
import boto3

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

def uploadFile(fileName):
    s3 = boto3.resource('s3')

    data = open(fileName, 'rb')
    s3.Bucket('pi-spy').put_object(ACL='public-read', ContentType='image/jpeg', Key='images/' + fileName, Body=data)

