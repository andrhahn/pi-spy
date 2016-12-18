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
            print 'capturing motion...'

            # noinspection PyRedeclaration
            last_capture_time = dt.datetime.now()

            image_stream = io.BytesIO()

            camera.capture(image_stream, format='jpeg', use_video_port=True)

            video_stream = io.BytesIO()

            camera.split_recording(video_stream)

            camera.wait_recording(5)

            camera.split_recording('/dev/null')

            fileName = last_capture_time.strftime('%Y-%m-%dT%H.%M.%S')

            image_stream.seek(0)
            fileservice.uploadFile(fileName + '.jpg', image_stream, 'image/jpeg')

            video_stream.seek(0)
            fileservice.uploadFile(fileName + '.h264', video_stream, 'video/h264')

            s3Link = 'http://s3.amazonaws.com/pi-spy/' + fileName + '.jpg'

            messageservice.sendMessage('Motion detected!\nhttp://s3.amazonaws.com/pi-spy/' + fileName + '.h264', 'http://s3.amazonaws.com/pi-spy/' + fileName + '.jpg')

            motion_detected = False

            print 'motion capture complete.'
        else:
            camera.wait_recording(1)
