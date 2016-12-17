from twilio.rest import TwilioRestClient
from ConfigParser import SafeConfigParser
import sys,os

print 'hello...'

sys.path.append(os.path.curdir)

parser = SafeConfigParser()
parser.read('../app_config')

print "hello: ",  parser.get('twilio', 'account_sid')

def sendMessage(body, to, media_url):
    accountSid = parser.get('twilio', 'account_sid')
    authToken = parser.get('twilio', 'auth_token')
    fromNumber = parser.get('twilio', 'from_number')

    client = TwilioRestClient(accountSid, authToken)

    client.messages.create(
        body=body,
        from_=fromNumber,
        to=to,
        media_url=media_url
    )
