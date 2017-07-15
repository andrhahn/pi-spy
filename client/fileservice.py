#!/usr/bin/python

import boto3

def uploadFile(bucketName, fileName, key, contentType):
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(bucketName)

    bucket.upload_file(fileName, key, ExtraArgs={'ACL': 'public-read', 'ContentType': contentType})
