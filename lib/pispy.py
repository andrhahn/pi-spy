#!/usr/bin/python

# noinspection PyUnresolvedReferences
import picamera
import picamera.array
import numpy as np
import datetime as dt
import io
import messageservice
import fileservice
import vimeo_client
import ConfigParser

parser = ConfigParser.SafeConfigParser()
parser.read('../app_config')

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

    #camera.start_recording('lowres.h264', splitter_port=2, resize=(320, 240))

    while True:
        if motion_detected:
            print 'capturing motion...'

            # noinspection PyRedeclaration
            last_capture_time = dt.datetime.now()

            fileName = last_capture_time.strftime('%Y-%m-%dT%H.%M.%S')

            #image_stream = io.BytesIO()

            #camera.capture(image_stream, format='jpeg', use_video_port=True)
            camera.capture(fileName + '.jpg', format='jpeg', use_video_port=True)

            video_stream = io.BytesIO()

            camera.split_recording(video_stream)

            camera.wait_recording(5)

            camera.split_recording('/dev/null')

            # image_stream.seek(0)
            # fileservice.uploadFile(fileName + '.jpg', image_stream, 'image/jpeg')
            #
            # video_stream.seek(0)
            # fileservice.uploadFile(fileName + '.h264', video_stream, 'video/h264')

            #s3_bucket_url = 'http://s3.amazonaws.com/' + parser.get('s3', 'bucket_name')

            #messageservice.sendMessage('Motion detected!\n' + s3_bucket_url + '/' + fileName + '.h264', s3_bucket_url + '/' + fileName + '.jpg')

            video_stream.seek(0)
            vimeo_client.sendMessage(fileName + '.jpg')


            motion_detected = False

            print 'motion capture complete.'
        else:
            camera.wait_recording(1)
