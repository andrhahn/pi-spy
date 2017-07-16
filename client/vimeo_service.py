#!/usr/bin/python

import vimeo

import config_service

def upload_file(file_name):
    vimeo_client = vimeo.VimeoClient(
        token=config_service.get_config('vimeo_token'),
        key=config_service.get_config('vimeo_key'),
        secret=config_service.get_config('vimeo_secret')
    )

    video_uri = vimeo_client.upload(file_name)

    vimeo_client.patch(video_uri, data={'name': 'Motion detected: ' + file_name, 'description': 'Motion detected...'})
