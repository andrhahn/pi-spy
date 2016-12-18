#!/usr/bin/python

# based on examples from:
# https://picamera.readthedocs.io/en/release-1.12/recipes2.html#custom-outputs

import picamera
import picamera.array
import numpy as np
from time import sleep
import messageservice
import fileservice

frames = 0
motion_detected = False
threshold = 10

class MyMotionDetector(picamera.array.PiMotionAnalysis):
    def analyse(self, a):
        global frames, motion_detected

        if frames < 10:
            frames = frames + 1
            return

        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
        ).clip(0, 255).astype(np.uint8)

        sum_ = (a > 60).sum()

        if sum_ > threshold:
            #print "sum", sum_
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
        if motion_detected:
            print 'motion detected. capturing image..'

            camera.stop_recording()

            motion_detected = False

            camera.capture('still.jpg', format='jpeg', use_video_port=True)

            #fileservice.uploadFile('still.jpg')

            #messageservice.sendMessage('Motion detected!', 'http://s3.amazonaws.com/pi-spy/images/still.jpg')

            #sleep(5)

            camera.start_recording('/dev/null', format='h264', motion_output=MyMotionDetector(camera))

        sleep(1)
