from twilio.rest import TwilioRestClient

accountSid = 'AC3371e1df0c1b2327c2beb171c22efb6e'
authToken = 'bf6e7a853c797ac0caa48823f814b927'

def sendMessage(body, to, media_url):
    client = TwilioRestClient(accountSid, authToken)

    myTwilioNumber = '+16122606647'

    myMessage = client.messages.create(
        body=body,
        from_=myTwilioNumber,
        to=to,
        media_url=media_url
    )
