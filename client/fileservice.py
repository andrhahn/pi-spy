#!/usr/bin/python

import boto3

def uploadFile(fileName, bucketName, keyName, contentType):
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(bucketName)

    bucket.upload_file(fileName, bucketName, keyName, ExtraArgs={'ACL': 'public-read', 'ContentType': contentType})
