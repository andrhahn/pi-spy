#!/usr/bin/python

from twilio.rest import TwilioRestClient
import config_service

def send_message(body, media_url):
    account_sid = config_service.get_config('twilio_account_sid')
    auth_token = config_service.get_config('twilio_auth_token')
    from_number = config_service.get_config('twilio_from_number')
    to_number = config_service.get_config('twilio_to_number')

    client = TwilioRestClient(account_sid, auth_token)

    client.messages.create(
        body=body,
        from_=from_number,
        to=to_number,
        media_url=media_url
    )
