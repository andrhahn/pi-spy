#!/usr/bin/python

import boto3

def uploadFile(bucketName, filePath, key, contentType):
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(bucketName)

    bucket.upload_file(filePath, key, ExtraArgs={'ACL': 'public-read', 'ContentType': contentType})
