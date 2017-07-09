# pi-spy client

### Getting Started

##### Setup
    sudo apt update
    
    sudo apt full-upgrade
    
    sudo pip install picamera
    
    mkdir -p /home/pi/pi-spy-files/logs
    
    mkdir -p /home/pi/pi-spy-files/images
    
    mkdir -p /home/pi/pi-spy-files/videos
    
    sudo crontab -e
    */1 * * * * python /home/pi/client/pi-spy/copy_files.py >> /home/pi/pi-spy-files/logs/copy_files.log 2>&1
    
##### Run client
    cd client

    python detect_motion.py
    
### License

[The MIT License](http://opensource.org/licenses/MIT)
