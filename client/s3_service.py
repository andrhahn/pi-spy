#!/usr/bin/python

import json
import boto3

def upload_file(bucketName, filePath, key, contentType):
    client = boto3.client('s3')

    response = client.put_object(Body=filePath, Bucket=bucketName, Key=key, ContentType=contentType, ACL='public-read')

    print '==s3 put_object resp: ' + json.dumps(response)

def send_email(subject, body, to_emails, from_email):
    client = boto3.client('ses')

    response = client.send_email(
        Source=from_email,
        Destination={
            'BccAddresses': [],
            'CcAddresses': [],
            'ToAddresses': to_emails
        },
        Message={
            'Subject': {
                'Data': subject,
                'Charset': 'UTF-8'
            },
            'Body': {
                'Html': {
                    'Data': body,
                    'Charset': 'UTF-8'
                }
            }
        },
        ReturnPath='andrhahn@hotmail.com'
    )

    print '==ses send_email resp: ' + json.dumps(response)
