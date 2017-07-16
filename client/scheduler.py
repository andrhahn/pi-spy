import schedule
import time
import os

process_new_images_path = '/home/pi/pi-spy-files/videos'

def process_new_images():
    print 'Running job: process_new_images'

    for filename in os.listdir(process_new_images_path):
        # do your stuff
        print 'File name: ' + filename

schedule.every(5).seconds.do(process_new_images)

while True:
    schedule.run_pending()

    time.sleep(1)
