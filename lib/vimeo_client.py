#!/usr/bin/python

import vimeo
import ConfigParser
import io

parser = ConfigParser.SafeConfigParser()
parser.read('../app_config')

def sendMessage(fileName):
    v = vimeo.VimeoClient(
        token=parser.get('vimeo', 'token'),
        key=parser.get('vimeo', 'key'),
        secret=parser.get('vimeo', 'secret')
    )

    video_uri = v.upload(fileName)

    v.patch(video_uri, data={'name': 'Motion deterted - ' + fileName, 'description': 'Motion detected...'})
