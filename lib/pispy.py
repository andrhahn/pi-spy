#!/usr/bin/python

# based on examples from:
# https://picamera.readthedocs.io/en/release-1.12/recipes2.html#custom-outputs

import picamera
import picamera.array
import numpy as np
import datetime as dt
import io
from time import sleep
import messageservice
import fileservice

threshold = 10
frames = 0
motion_detected = False
last_still_capture_time = dt.datetime.now()

class MyMotionDetector(picamera.array.PiMotionAnalysis):
    def analyse(self, a):
        global frames, motion_detected, last_still_capture_time

        if dt.datetime.now() > last_still_capture_time + dt.timedelta(seconds=5):
            if frames < 10:
                frames = frames + 1
                return

            a = np.sqrt(
                np.square(a['x'].astype(np.float)) +
                np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)

            sum_ = (a > 60).sum()

            if sum_ > threshold:
                print "sum", sum_
                motion_detected = True

def record(camera):
    print 'recording started...'

    camera.start_recording('/dev/null', format='h264', motion_output=MyMotionDetector(camera))

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 30
    camera.vflip = True
    camera.hflip = True

    print 'waiting for motion...'

    camera.start_recording('/dev/null', format='h264', motion_output=MyMotionDetector(camera))

    while True:
        while not motion_detected:
            camera.wait_recording(1)

        print 'motion detected...'

        camera.stop_recording()

        # motion_detected = False

        last_still_capture_time = dt.datetime.now()

        stream = io.BytesIO()

        camera.capture(stream, format='jpeg', use_video_port=True)

        print 'image captured...'

        fileservice.uploadFile(stream)

        #messageservice.sendMessage('Motion detected!', 'http://s3.amazonaws.com/pi-spy/images/still.jpg')

        camera.start_recording('/dev/null', format='h264', motion_output=MyMotionDetector(camera))

        motion_detected = False
