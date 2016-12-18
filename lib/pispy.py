#!/usr/bin/python

# noinspection PyUnresolvedReferences
import picamera
import picamera.array
import numpy as np
import datetime as dt
import io
import messageservice
import fileservice

threshold = 10
motion_detected = False
last_capture_time = dt.datetime.now()

class MyMotionDetector(picamera.array.PiMotionAnalysis):
    def analyse(self, a):
        global motion_detected, last_capture_time

        if dt.datetime.now() > last_capture_time + dt.timedelta(seconds=5):
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
        if motion_detected:
            # while not motion_detected:
            #     camera.wait_recording(1)

            print 'motion detected...'

            # camera.stop_recording()

            # noinspection PyRedeclaration
            last_capture_time = dt.datetime.now()

            stream = io.BytesIO()

            camera.split_recording(stream)

            # camera.start_recording(stream, format='h264', quality=20)
            camera.wait_recording(5)
            camera.stop_recording()

            print 'video captured...'

            stream.seek(0)

            fileName = last_capture_time.strftime('%Y-%m-%dT%H.%M.%S') + '.h264'

            fileservice.uploadFile(fileName, stream, 'video/h264')

            messageservice.sendMessage('Motion detected!', 'http://s3.amazonaws.com/pi-spy/' + fileName)

            camera.start_recording('/dev/null', format='h264', motion_output=MyMotionDetector(camera))

            motion_detected = False
        else:
            camera.wait_recording(1)
