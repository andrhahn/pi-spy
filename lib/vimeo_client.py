#!/usr/bin/python

import vimeo
import ConfigParser

parser = ConfigParser.SafeConfigParser()
parser.read('../app_config')

def sendMessage(body, media_url):
    v = vimeo.VimeoClient(
        token=parser.get('vimeo', 'token'),
        key=parser.get('vimeo', 'key'),
        secret=parser.get('vimeo', 'secret')
    )

    # Make the request to the server for the "/me" endpoint.
    about_me = v.get('/me')

    assert about_me.status_code == 200  # Make sure we got back a successful response.
    print about_me.json()   # Load the body's JSON data.
