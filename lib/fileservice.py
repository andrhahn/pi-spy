#!/usr/bin/python

import boto3

def uploadFile(fileName):
    s3 = boto3.resource('s3')

    data = open(fileName, 'rb')
    s3.Bucket('pi-spy').put_object(ACL='public-read', ContentType='image/jpeg', Key='images/' + fileName, Body=data)
