import io
import picamera
import picamera.array
import numpy as np
from time import sleep

frames = 0
motion_detected = False

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
        # If there're more than 10 vectors with a magnitude greater than 60, then say we've detected motion
        if (a > 60).sum() > 10:
            print('Motion detected!')
            motion_detected = True

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 30

    camera.vflip = True
    camera.hflip = True

    print 'starting recording...'

    camera.start_recording('/dev/null', format='h264', motion_output=MyMotionDetector(camera))

    while True:
        while not motion_detected:
            camera.wait_recording(1)

        camera.stop_recording()

        motion_detected = False

        # todo - once motion is detected, take video stream from above and write it
        # to a notification stream ie. aws

        stream = io.BytesIO()

        print 'capturing still image...'
        camera.capture('still.jpg', format='jpeg', use_video_port=True)
        #camera.capture(stream, format='jpeg', use_video_port=True)

        #wait to start recording back up
        sleep(5)

        print 'starting recording back up...'
        camera.start_recording('/dev/null', format='h264', motion_output=MyMotionDetector(camera))
