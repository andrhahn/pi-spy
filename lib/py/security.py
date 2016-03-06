import io
import time
import random
import picamera

def write_now():
    print "in Write now"
    # Randomly return True (like a fake motion detection routine)
    return random.randint(0, 10) == 0

def write_video(stream):
    print('Writing video!')
    with stream.lock:
        # Find the first header frame in the video
        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
        # Write the rest of the stream to disk
        with io.open('/home/pi/projects/pycam/motion.h264', 'wb') as output:
            output.write(stream.read())

print "welcome to pycam"

with picamera.PiCamera() as camera:
    time.sleep(1) # let camera warm up

    print "camera started..."

    #camera.framerate = 10
    camera.resolution = (640, 480)
    camera.vflip = True

    stream = picamera.PiCameraCircularIO(camera, seconds=20)
    camera.start_recording(stream, format='h264')
    try:
        while True:
            print "polling started..."
            camera.wait_recording(1)

            if write_now():
                print "detected motion. about to capture 10 seconds of video in 5 seconds..."

                time.sleep(5)

                camera.wait_recording(10)

                print "recording done. about to write video..."
                write_video(stream)

                print "writing done. about to sleep for 120 seconds..."

                time.sleep(120)
            else:
                print "motion not detected..."
    finally:
        print "Stop recording"
        camera.stop_recording()
