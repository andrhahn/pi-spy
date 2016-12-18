#!/usr/bin/python

import boto3

def uploadFile(fileName, data):
    s3 = boto3.resource('s3')

    bucket = s3.Bucket('pi-spy')

    bucket.upload_fileobj(Fileobj=data, Key=fileName, ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'})
