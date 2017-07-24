#!/usr/bin/python

import json
import boto3
import logging
import config_service

log_level = config_service.get_config("log_level")
logging.basicConfig(level=getattr(logging, log_level))

def upload_file(bucket, body, key, content_type):
    client = boto3.client('s3')

    response = client.put_object(Body=body, Bucket=bucket, Key=key, ContentType=content_type, ACL='public-read')

    logging.debug('3 put_object resp: ' + json.dumps(response))

def send_email(subject, body, to_emails):
    client = boto3.client('ses')

    response = client.send_email(
        Source='info@scranthdaddy.com',
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
        ReturnPath='info@scranthdaddy.com'
    )

    logging.debug('ses send_email resp: ' + json.dumps(response))
