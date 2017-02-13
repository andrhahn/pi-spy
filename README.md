# pi-spy

Pure python Motion detector for Raspberry Pi 3 Model B with camera module

Detects motion then uplaods image and video to S3 or Vimeo then sends SMS message via Twilio

Requires Amazon S3 and Twilio accounts (both are free)

### Getting Started

##### Setup
    sudo apt update
    
    sudo apt full-upgrade
    
    sudo pip install boto3
    
    sudo pip install PyVimeo

    sudo pip install twilio
    
    configure aws credentials - ex. create ~/.aws/credentials
    
    create and configure app_config from app_config_template

##### Run
    python pispy.py
    
### License

[The MIT License](http://opensource.org/licenses/MIT)
