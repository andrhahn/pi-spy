from twilio.rest import TwilioRestClient

accountSid = ''
authToken = ''

def sendMessage(body, to, media_url):
    client = TwilioRestClient(accountSid, authToken)

    myTwilioNumber = ''

    client.messages.create(
        body=body,
        from_=myTwilioNumber,
        to=to,
        media_url=media_url
    )
