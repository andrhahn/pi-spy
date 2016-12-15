#!/usr/bin/python

import io
import picamera
import ImageChops
import math, operator
from PIL import Image
from time import sleep

threshold = 100

prior_image = None

def calculateRms(im1, im2):
    diff = ImageChops.difference(im1, im2)
    h = diff.histogram()
    sq = (value*((idx%256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
    return rms

def detect_motion(camera):
    global prior_image

    stream = io.BytesIO()

    camera.capture(stream, format='jpeg', use_video_port=True)

    stream.seek(0)

    if prior_image is None:
        prior_image = Image.open(stream)

        return False
    else:
        current_image = Image.open(stream)

        rms = calculateRms(current_image, prior_image)

        if rms > threshold:
            print 'motion detected!'
            result = True
        else:
            result = False

        prior_image = current_image

        return result

def write_video(stream):
    with io.open('before.h264', 'wb') as output:
        for frame in stream.frames:
            if frame.header:
                stream.seek(frame.position)
                break

        while True:
            buf = stream.read1()

            if not buf:
                break

            output.write(buf)

    stream.seek(0)
    stream.truncate()

with picamera.PiCamera() as camera:
    sleep(2)

    camera.resolution = (1280, 720)

    stream = picamera.PiCameraCircularIO(camera, seconds=10)

    print 'starting recording...'

    camera.start_recording(stream, format='h264')

    try:
        while True:
            camera.wait_recording(1)

            if detect_motion(camera):
                camera.split_recording('after.h264')

                write_video(stream)

                while detect_motion(camera):
                    camera.wait_recording(1)

                camera.split_recording(stream)
    finally:
        camera.stop_recording()
