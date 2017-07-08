# pi-spy

Pure python Motion detector for Raspberry Pi 3 Model B with camera module

Detects motion then uplaods image and video to S3 or Vimeo then sends SMS message via Twilio

Requires Amazon S3 and Twilio accounts (both are free)

### Getting Started

##### RPI Setup
    sudo apt update
    
    sudo apt full-upgrade
    
    sudo apt-get install python-picamera
    
    sudo pip install boto3
    
    sudo pip install PyVimeo

    sudo pip install twilio
    
    create app_config from app_config_template
    
    create ~/.aws/credentials from credentials_template
    
##### Run pispy
    cd pi-spy

    (git pull && cd lib && python pispy.py)
 
##### Run test
    cd pi-spy

    (git pull && cd lib && python test.py)
    
### License

[The MIT License](http://opensource.org/licenses/MIT)
