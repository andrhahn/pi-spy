#!/usr/bin/python

import io
import picamera, picamera.array
import numpy as np
import math, operator
from PIL import Image
from PIL import ImageChops
from time import sleep

prior_image = None

def test():
    image1 = Image.open("file1.jpg")
    image2 = Image.open("file2.jpg")

    print compareNumpyArrays(np.array(image1), np.array(image2))


def compareImageChops(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None

def compareNumpyArrays(a, b, threshold=10):
    # return (np.abs(a.astype(np.int16) - b.astype(np.int16)) > threshold).any()

    # Ensure a and b are types which won't overflow on subtraction
    a = a.astype(np.int16)
    b = b.astype(np.int16)
    # Create an array from the absolute difference of a and b
    c = np.abs(a - b)
    # Create an array of truth values indicating whether any
    # absolute differences are greater than the threshold
    c = c > threshold
    # Return whether any values are greater than the threshold

    return c.any()

def calculateRms(im1, im2):
    diff = ImageChops.difference(im1, im2)

    h = diff.histogram()

    sq = (value*((idx%256)**2) for idx, value in enumerate(h))

    sum_of_squares = sum(sq)

    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))

    # h1 = im1.histogram()
    # h2 = im2.histogram()
    #
    # rms = math.sqrt(reduce(operator.add, map(lambda a,b: (a-b)**2, h1, h2))/len(h1))

    print "rms: ", rms

    return rms

def comparePixels(data1, data2):
    threshold = 10
    sensitivity = 25

    changedPixels = 0

    for x in range(0, 1024):
        for y in range(0, 768):
            # Just check green channel as it's the highest quality channel
            # pixColor = 1 # red=0 green=1 blue=2
            diff = abs(data1[x,y][1] - data2[x,y][1])

            print "diff: ", diff

            if diff > threshold:
                changedPixels += 1

            if changedPixels > sensitivity:
                break  # break inner loop

        if changedPixels > sensitivity:
            break  #break outer loop

    print "changed pixels: ", changedPixels

    if changedPixels > sensitivity:
        return True
    else:
        return False

def detect_motion(camera):
    global prior_image

    # stream = io.BytesIO()

    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='rgb', use_video_port=True)

        stream.seek(0)

        if prior_image is None:
            #prior_image = Image.open(stream)
            prior_image = stream.array

            return False
        else:
            #current_image = Image.open(stream)
            current_image = stream.array

            # result = calculateRms(current_image, prior_image) > threshold

            # result = campareImageChops(current_image, prior_image)

            # result = compareNumpyArrays(np.array(current_image), np.array(prior_image))

            result = comparePixels(current_image, prior_image)

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
    print 'started pispy'

    #sleep(2)
    sleep(10)

    camera.resolution = (1024, 768)
    camera.vflip = True
    camera.hflip = True

    stream = picamera.PiCameraCircularIO(camera, seconds=10)

    camera.start_recording(stream, format='h264')

    try:
        while True:
            camera.wait_recording(1)

            if detect_motion(camera):
                print 'started recording motion'
                camera.split_recording('after.h264')

                write_video(stream)

                while detect_motion(camera):
                    camera.wait_recording(1)

                print 'stopped recording motion'
                camera.split_recording(stream)
    finally:
        camera.stop_recording()
