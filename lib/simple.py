#!/usr/bin/python

import time
import datetime
import picamera

with picamera.PiCamera() as camera:
    time.sleep(2) # let camera warm up

    camera.start_preview()

    camera.resolution = (640, 480)
    camera.vflip = True

    # formats as /home/pi/2016-03-01_19-17-58.h264
    filename = datetime.datetime.now().strftime("/home/pi/%Y-%m-%d_%H-%M-%S.h264")

    camera.start_recording(filename)

    camera.wait_recording(5)

    camera.stop_recording()

    camera.stop_preview()
