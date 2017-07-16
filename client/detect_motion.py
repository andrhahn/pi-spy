import io
import os
import picamera
import datetime as dt
import uuid
from PIL import Image
from PIL import ImageChops
from PIL import ImageOps
from PIL import ImageDraw
import ConfigParser

import messageservice
import fileservice

parser = ConfigParser.SafeConfigParser()
parser.read('../app_config')

images_file_path = '/home/pi/pi-spy-files/images'
prior_image = None
captured_image = None
captured_image_file_names = []
rect_coords = None

def detect_motion(camera):
    global images_file_path
    global prior_image
    global captured_image
    global captured_image_file_names
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

            # draw box around the image
            ImageDraw.Draw(captured_image).rectangle(rect_coords, outline="yellow", fill=None)

            image_guid = str(uuid.uuid4())

            captured_image_file_name = image_guid + '.jpg'

            # save file to file system
            captured_image.save(images_file_path + '/' + captured_image_file_name)

            print 'saved image to images folder'

            if len(captured_image_file_names) < 5:
                captured_image_file_names.append(captured_image_file_name)

            prior_image = current_image

            return True
        else:
            return False

def write_video(stream, video_guid):
    with io.open('/home/pi/pi-spy-files/videos/before_' + video_guid + '.h264', 'wb') as output:
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

                captured_image_file_names = []

                video_guid = str(uuid.uuid4())

                # if motion is detected, split the recording to record the frames "after" motion
                camera.split_recording('/home/pi/pi-spy-files/videos/after_' + video_guid + '.h264')

                # write the 10 seconds "before" motion to disk as well
                write_video(stream, video_guid)

                # record video as long as there is motion being detected
                while detect_motion(camera):
                    camera.wait_recording(1)

                # once motion is no longer detected, split recording back to the in-memory circular buffer
                camera.split_recording(stream)

                #s3_bucket_name = parser.get('s3', 'bucket_name')

                for image_file_name in captured_image_file_names:
                    print '===image file in array:' + image_file_name

                    # upload image to s3
                    #fileservice.uploadFile(s3_bucket_name, filePath + '/' + image_file_name, image_file_name, 'image/jpeg')

                    print 'Image uploaded to s3...'
#
                # send mms # todo send list
                #messageservice.sendMessage('Motion detected!', 'http://s3.amazonaws.com/' + s3_bucket_name + '/' + fileName)

                print 'Twilio message sent...'

                print 'Recording motion - COMPLETED'
    finally:
        camera.stop_recording()
