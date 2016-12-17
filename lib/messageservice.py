from twilio.rest import TwilioRestClient

accountSid = 'AC3371e1df0c1b2327c2beb171c22efb6e'
authToken = 'bf6e7a853c797ac0caa48823f814b927'

client = TwilioRestClient(accountSid, authToken)

myTwilioNumber = '+16513532651'
destCellPhone = '+16513532651'

myMessage = client.messages.create(body ="Motion detected!", from_=myTwilioNumber, to=destCellPhone)

# media = "http://www.mattmakai.com/source/static/img/work/fsp-logo.png"

# client.messages.create(to="+19732644152", from_="+12023358536",
#                        body="MMS via Python? Nice!", media_url=media)
