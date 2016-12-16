#!/usr/bin/python

import math, operator
import numpy as np
from PIL import Image
from PIL import ImageChops

threshold = 100

def compare(a, b, threshold=10):
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
    return rms

def hello():
    image1 = Image.open("file1.jpg")
    image2 = Image.open("file2.jpg")

    print compare(np.array(image1), np.array(image2))
