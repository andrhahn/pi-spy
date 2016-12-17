#!/usr/bin/python

from twilio.rest import TwilioRestClient
from ConfigParser import SafeConfigParser
import sys, os

sys.path.append(os.path.curdir)

parser = SafeConfigParser()
parser.read('../app_config')

def sendMessage(body, media_url):
    accountSid = parser.get('twilio', 'account_sid')
    authToken = parser.get('twilio', 'auth_token')
    fromNumber = parser.get('twilio', 'from_number')
    toNumber = parser.get('twilio', 'to_number')

    client = TwilioRestClient(accountSid, authToken)

    client.messages.create(
        body=body,
        from_=fromNumber,
        to=toNumber,
        media_url=media_url
    )
