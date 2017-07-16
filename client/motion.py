#!/usr/bin/python

import os
import io
import threading
import picamera
import uuid
from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw
from PIL import ImageOps

import config_service
import s3_service
import twilio_service
import vimeo_service

images_path = config_service.get_config("images_path")
videos_path = config_service.get_config("videos_path")
logs_path = config_service.get_config("logs_path")

prior_image = None
captured_image = None
captured_image_file_names = []
rect_coords = None

def create_dirs():
    create_dir(images_path)
    create_dir(videos_path)
    create_dir(logs_path)

def create_dir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

def save_image(file_name):
    captured_image.save(images_path + '/' + file_name)

    print 'Saved image: ' + images_path + '/' + file_name

def process_images(captured_image_file_names, video_guid):
    s3_host_name = 'http://s3.amazonaws.com'

    s3_bucket_name = config_service.get_config('s3_bucket_name')

    media_urls = []

    for image_file_name in captured_image_file_names:
        # upload image to s3
        key = 'images/' + image_file_name

        s3_service.upload_file(s3_bucket_name, images_path + '/' + image_file_name, key, 'image/jpeg')

        media_url = s3_host_name + '/' + s3_bucket_name + '/' + key

        print 'Uploaded image to s3: ' + media_url

        media_urls.append(media_url)

    # send mms
    twilio_service.send_message('Motion detected!', media_urls)

    # upload video to twilio # todo: concat and upload before.h264
    vimeo_service.upload_file(videos_path + '/after_' + video_guid + '.h264')

    print 'Twilio message sent...'

def detect_motion(camera):
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

        diff_image = ImageOps.posterize(ImageOps.grayscale(ImageChops.difference(prior_image, current_image)), 1)

        rect_coords = diff_image.getbbox()

        if rect_coords != None:
            captured_image = current_image.copy()

            # draw box around the image
            ImageDraw.Draw(captured_image).rectangle(rect_coords, outline="yellow", fill=None)

            image_guid = str(uuid.uuid4())

            captured_image_file_name = image_guid + '.jpg'

            # save file to file system
            save_image_thread = threading.Thread(target=save_image, args=(captured_image_file_name,))

            save_image_thread.start()

            if len(captured_image_file_names) < 5:
                captured_image_file_names.append(captured_image_file_name)

            prior_image = current_image

            return True
        else:
            return False


def write_video(stream, video_guid):
    with io.open(videos_path + '/before_' + video_guid + '.h264', 'wb') as output:
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
    create_dirs()

    print 'Started pi-cam'

    camera.resolution = (1280, 720)
    camera.vflip = True
    camera.hflip = True

    stream = picamera.PiCameraCircularIO(camera, seconds=10)

    camera.start_recording(stream, format='h264')

    try:
        while True:
            print 'Polling for motion'

            camera.wait_recording(1)

            if detect_motion(camera):
                print 'Recording motion - started'

                captured_image_file_names = []

                video_guid = str(uuid.uuid4())

                # if motion is detected, split the recording to record the frames "after" motion
                camera.split_recording(videos_path + '/after_' + video_guid + '.h264')

                # write the 10 seconds "before" motion to disk as well
                write_video(stream, video_guid)

                # record video as long as there is motion being detected
                while detect_motion(camera):
                    camera.wait_recording(1)

                print 'Recording motion - completed'

                # once motion is no longer detected, split recording back to the in-memory circular buffer
                camera.split_recording(stream)

                # process images in a thread
                process_images_thread = threading.Thread(target=process_images, args=(list(captured_image_file_names),video_guid,))

                process_images_thread.start()
    finally:
        camera.stop_recording()
