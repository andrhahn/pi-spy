import io
import picamera
import datetime as dt
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
        # compare current_image with prior_image and make a box around the change
        diff_image = ImageOps.posterize(ImageOps.grayscale(ImageChops.difference(prior_image, current_image)) ,1)

        rect_coords = diff_image.getbbox()

        if rect_coords != None:
            left = rect_coords[0]
            upper = rect_coords[1]
            right = rect_coords[2]
            lower = rect_coords[3]

            #print '===left: ', left
            #print '===upper: ', upper
            #print '===right: ', right
            #print '===lower: ', lower

            width = right - left
            height = lower - upper

            #print '===width: ', width
            #print '===height: ', height

            area = width * height

            print '===area: ', area

            print '===motion detected. saving image...'

            # clone current_image
            cloned_current_image = current_image.copy()

            ImageDraw.Draw(cloned_current_image).rectangle(rect_coords, outline="yellow", fill=None)

            capture_time = dt.datetime.now()

            fileName = '/home/pi/images/' + capture_time.strftime('%Y-%m-%dT%H.%M.%S') + '.jpg'

            cloned_current_image.save(fileName)

            # once motion detection is done, make the prior image the current
            prior_image = current_image

            return True
        else:
            return False

def write_video(stream):
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

    stream.seek(0)
    stream.truncate()

with picamera.PiCamera() as camera:
    print 'started app...'

    camera.resolution = (1280, 720)
    camera.vflip = True
    camera.hflip = True
    stream = picamera.PiCameraCircularIO(camera, seconds=10)
    camera.start_recording(stream, format='h264')
    try:
        while True:
            camera.wait_recording(1)
            if detect_motion(camera):
                #print('Motion detected!')
                # As soon as we detect motion, split the recording to
                # record the frames "after" motion
                camera.split_recording('after.h264')
                # Write the 10 seconds "before" motion to disk as well
                write_video(stream)
                # Wait until motion is no longer detected, then split
                # recording back to the in-memory circular buffer
                while detect_motion(camera):
                    camera.wait_recording(1)
                #print('Motion stopped!')
                camera.split_recording(stream)

                # todo: write the saved video somewhere...
    finally:
        camera.stop_recording()
