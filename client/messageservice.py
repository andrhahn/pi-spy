#!/usr/bin/python

from twilio.rest import TwilioRestClient
import configservice

def sendMessage(body, media_url):
    account_sid = configservice.get_config('twilio_account_sid')
    auth_token = configservice.get_config('twilio_auth_token')
    from_number = configservice.get_config('twilio_from_number')
    to_number = configservice.get_config('twilio_to_number')

    client = TwilioRestClient(account_sid, auth_token)

    client.messages.create(
        body=body,
        from_=from_number,
        to=to_number,
        media_url=media_url
    )
