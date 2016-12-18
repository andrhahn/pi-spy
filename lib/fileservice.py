#!/usr/bin/python

import boto3

def uploadFile(data):
    s3 = boto3.resource('s3')

    bucket = s3.Bucket('pi-spy')

    bucket.upload_fileobj(data, 'images/test2.jpg')
