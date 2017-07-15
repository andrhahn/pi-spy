import io
import picamera
import datetime as dt
from PIL import Image
from PIL import ImageChops
from PIL import ImageOps
from PIL import ImageDraw
import ConfigParser

import messageservice
import fileservice

parser = ConfigParser.SafeConfigParser()
parser.read('../app_config')

prior_image = None
captured_image = None
rect_coords = None

def detect_motion(camera):
    global prior_image
    global captured_image
    global rect_coords

    stream = io.BytesIO()

    camera.capture(stream, format='jpeg', use_video_port=True)

    stream.seek(0)

    if prior_image is None:
        prior_image = Image.open(stream)

        return False
    else:
        current_image = Image.open(stream)

        diff_image = ImageOps.posterize(ImageOps.grayscale(ImageChops.difference(prior_image, current_image)) ,1)

        rect_coords = diff_image.getbbox()

        if rect_coords != None:
            captured_image = current_image.copy()

            prior_image = current_image

            return True
        else:
            return False

def write_video(stream, capture_time):
    with io.open('/home/pi/pi-spy-files/videos/before_' + capture_time.strftime('%Y-%m-%dT%H.%M.%S') + '.h264', 'wb') as output:
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
                print 'Recording motion - STARTED'

                capture_time = dt.datetime.now()

                # if motion is detected, split the recording to record the frames "after" motion
                camera.split_recording('/home/pi/pi-spy-files/videos/after_' + capture_time.strftime('%Y-%m-%dT%H.%M.%S') + '.h264')

                # write the 10 seconds "before" motion to disk as well
                write_video(stream, capture_time)

                # draw box around the image
                ImageDraw.Draw(captured_image).rectangle(rect_coords, outline="yellow", fill=None)

                fileName = capture_time.strftime('%Y-%m-%dT%H.%M.%S') + '.jpg'

                filePath = '/home/pi/images/' + fileName

                # save file to filesystem
                captured_image.save(fileName)

                # upload image to s3
                s3_bucket_name = parser.get('s3', 'bucket_name')

                fileservice.uploadFile(filePath, s3_bucket_name, fileName, 'image/jpeg')

                print 'Image uploaded to s3...'

                # send mms
                messageservice.sendMessage('Motion detected!', 'http://s3.amazonaws.com/' + s3_bucket_name + '/' + fileName)

                print 'Twilio message sent...'

                # record video as long as there is motion being detected
                while detect_motion(camera):
                    camera.wait_recording(1)

                # once motion is no longer detected, split recording back to the in-memory circular buffer
                camera.split_recording(stream)

                print 'Recording motion - COMPLETED'
    finally:
        camera.stop_recording()
