#!/usr/bin/python

import os
import time
import schedule
import config_service

def process_new_images():
    print 'Running job: process_new_images at ' + time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())

    images_path = config_service.get_config('images_path')

    for filename in os.listdir(images_path):
        print 'File name: ' + filename

schedule.every(10).seconds.do(process_new_images)

while True:
    schedule.run_pending()

    time.sleep(1)
