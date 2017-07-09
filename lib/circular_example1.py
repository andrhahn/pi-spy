import io
import random
import picamera
from PIL import Image
from PIL import ImageChops
from PIL import ImageOps
from PIL import ImageDraw

prior_image = None

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
        # Compare current_image to prior_image to detect motion. This is
        # left as an exercise for the reader!

        #diff = ImageChops.difference(current_image, prior_image)
        #print '==diff: ', diff

        #compare current image with Master and make a box around the change
        diff_image = ImageOps.posterize(ImageOps.grayscale(ImageChops.difference(prior_image, current_image)) ,1)

        rect_coords = diff_image.getbbox()

        if rect_coords != None:
            print '===rectangle found.  about to draw yellow line'

            ImageDraw.Draw(current_image).rectangle(rect_coords, outline="yellow", fill=None)

            print 'about to save image'

            current_image.save('/home/pi/result.jpeg')

            print 'saved image'
            # Once motion detection is done, make the prior image the current
            #prior_image = current_image

            return True
        else:
            print '===rectangle not found'

            return False

        #result = False
        #result = random.randint(0, 10) == 0

        # Once motion detection is done, make the prior image the current
        #prior_image = current_image
        #return result

def write_video(stream):
    # Write the entire content of the circular buffer to disk. No need to
    # lock the stream here as we're definitely not writing to it
    # simultaneously
    with io.open('before.h264', 'wb') as output:
        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
        while True:
            buf = stream.read1()
            if not buf:
                break
            output.write(buf)
    # Wipe the circular stream once we're done
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
                # As soon as we detect motion, split the recording to
                # record the frames "after" motion
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
