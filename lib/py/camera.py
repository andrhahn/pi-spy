#!/usr/bin/python

import io
import picamera
import numpy as np

threshold = 10

previous_image_data = None

def changed(a, b):
    return (np.abs(a.astype(np.int16) - b.astype(np.int16)) > threshold).any()

def detect_motion(camera):
    global previous_image_data

    stream = io.BytesIO()

    camera.capture(stream, format='jpeg', use_video_port=True)

    stream.seek(0)

    if previous_image_data is None:
        previous_image_data = np.fromstring(stream.getvalue(), dtype=np.uint8)

        return False
    else:
        current_image_data = np.fromstring(stream.getvalue(), dtype=np.uint8)

        result = changed(current_image_data, previous_image_data)

        previous_image_data = current_image_data

        return result

def write_video(stream):
    # Write the entire content of the circular buffer to disk
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
    camera.resolution = (1280, 720)

    stream = picamera.PiCameraCircularIO(camera, seconds=10)

    camera.start_recording(stream, format='h264')

    try:
        while True:
            camera.wait_recording(1)
            if detect_motion(camera):
                print('Motion detected!')

                # As soon as we detect motion, split the recording to record the frames "after" motion
                camera.split_recording('after.h264')

                # Write the 10 seconds "before" motion to disk as well
                write_video(stream)

                # Wait until motion is no longer detected, then split
                # recording back to the in-memory circular buffer
                while detect_motion(camera):
                    camera.wait_recording(1)

                print('Motion stopped!')

                camera.split_recording(stream)
    finally:
        camera.stop_recording()
