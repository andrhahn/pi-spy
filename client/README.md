# pi-spy client

###### The client code runs on the rpi camera and consists of two processes:
    1) motion.py - detects motion
    2) scheduler.py - regularly polls to detect any new files

The motion.py process is focused on detecting motion.  It is separated out from the scheduler.py process so it does not get bogged down uploading files and sending notifications.  We want motion detection to be as lean and fast as possible.
 
The scheduler.py process is focused on polling for any newly captured motion detection images, and then uploading those images and sending out a notification.

##### Setup
    sudo apt update
    
    sudo apt full-upgrade
    
    sudo pip install picamera
    
    sudo pip install schedule
    
    sudo pip install twilio
        
    sudo pip install boto3
    
    mkdir -p /home/pi/pi-spy-files/logs
    
    mkdir -p /home/pi/pi-spy-files/images
    
    mkdir -p /home/pi/pi-spy-files/videos
    
##### Run
    python motion.py
    
    python scheduler.py
    
### License

[The MIT License](http://opensource.org/licenses/MIT)
