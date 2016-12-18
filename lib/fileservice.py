#!/usr/bin/python

import boto3

def uploadFile(data):
    s3 = boto3.resource('s3')

    bucket = s3.Bucket('pi-spy')

    # s3.Bucket('pi-spy')
    # .put_object(ACL='public-read', ContentType='image/jpeg', Key='images/' + fileName, Body=data)

    bucket.upload_fileobj(Fileobj=data, Key='images/test3.jpg', ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'})
