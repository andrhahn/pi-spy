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

def process_images(captured_image_file_names, video_guid):
    s3_host_name = 'http://s3.amazonaws.com'

    s3_bucket_name = config_service.get_config('s3_bucket_name')

    media_urls = []

    for image_file_name in captured_image_file_names:
        key = 'images/' + image_file_name

        # upload image to s3
        s3_service.upload_file(s3_bucket_name, images_path + '/' + image_file_name, key, 'image/jpeg')

        media_url = s3_host_name + '/' + s3_bucket_name + '/' + key

        media_urls.append(media_url)

    # upload videos to s3
    before_file_name = 'before_' + video_guid + '.h264'
    after_file_name = 'after_' + video_guid + '.h264'

    s3_service.upload_file(s3_bucket_name, videos_path + '/' + before_file_name, 'videos/' + before_file_name, 'video/h264')
    s3_service.upload_file(s3_bucket_name, videos_path + '/' + after_file_name, 'videos/' + after_file_name, 'video/h264')

    # send ses email
    # body = 'This message body contains HTML formatting. It can, contain links like this: <a class="ulink" href="http://docs.aws.amazon.com/ses/latest/DeveloperGuide" target="_blank">Amazon SES Developer Guide</a>.',
    body = 'This message body contains HTML forhttp://docs.aws.amazon.com/ses/latest/DeveloperGuide" target="_blank">Amazon SES Developer Guide</a>.'

    to_emails = ['andrhahn@hotmail.com']

    s3_service.send_email('Motion detected', body, to_emails, 'andrhahn@hotmail.com')

    print 'Image and Video processing complete.'

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

    # creates a "before" stream which only holds 10 total seconds of data
    stream = picamera.PiCameraCircularIO(camera, seconds=10)

    # start recording to "before" stream
    camera.start_recording(stream, format='h264')

    try:
        while True:
            print 'Polling for motion...'

            camera.wait_recording(1)

            if detect_motion(camera):
                print 'Recording motion - started'

                captured_image_file_names = []

                video_guid = str(uuid.uuid4())

                # once motion is detected, start recording "after" video data directly to disk
                # this recording of "after" video will continue to record to disk until motion is no longer detected
                camera.split_recording(videos_path + '/after_' + video_guid + '.h264')

                # write "before" stream data (the last 10 seconds) to disk
                write_video(stream, video_guid)

                # keep recording to "after" stream until motion stops
                while detect_motion(camera):
                    camera.wait_recording(1)

                print 'Recording motion - completed'

                # once motion is done, start recording to "before" stream again
                camera.split_recording(stream)

                # process images in a separate thread
                process_images_thread = threading.Thread(target=process_images, args=(list(captured_image_file_names),video_guid,))

                process_images_thread.start()
    finally:
        camera.stop_recording()
