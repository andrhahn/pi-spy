#!/usr/bin/python

import math, operator
from PIL import Image
from PIL import ImageChops

threshold = 100

def calculateRms(im1, im2):
    diff = ImageChops.difference(im1, im2)
    h = diff.histogram()
    sq = (value*((idx%256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
    return rms

def hello():
    image1 = Image.open("file1.jpg")
    image2 = Image.open("file2.jpg")

    rms = calculateRms(image1, image2)

    if rms > threshold:
        print 'motion detected!'
    else:
        print 'no motion detected!'
