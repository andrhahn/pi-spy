#!/usr/bin/python

import boto3

def uploadFile(bucketName, fileName, data, contentType):
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(bucketName)

    bucket.upload_fileobj(Fileobj=data, Key=fileName, ExtraArgs={'ACL': 'public-read', 'ContentType': contentType})
