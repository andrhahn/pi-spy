#!/usr/bin/python

import vimeo
import ConfigParser

parser = ConfigParser.SafeConfigParser()
parser.read('../app_config')

def sendMessage(fileName, data):
    v = vimeo.VimeoClient(
        token=parser.get('vimeo', 'token'),
        key=parser.get('vimeo', 'key'),
        secret=parser.get('vimeo', 'secret')
    )

    #video_uri = v.upload('your-filename.mp4')
    video_uri = v.upload(data)

    v.patch(video_uri, data={'name': 'Motion deterted - ' + fileName, 'description': 'Motion detected...'})
