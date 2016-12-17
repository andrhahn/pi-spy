# pi-spy

Pure python Motion detector and notifier for Raspberry Pi 3 Model B with camera module

On motion detection an image is captured and uploaded to S3 and an SMS message is sent via Twilio

Requires Amazon S3 and Twilio accounts (both are free)

### Getting Started

##### Setup
    sudo apt update
    
    sudo apt full-upgrade
    
    sudo pip install boto3

    sudo pip install twilio
    
    configure aws credentials - ex. create ~/.aws/credentials
    
    create and configure app_config file from app_config_template

##### Run
    python detect_motion.py
    
### License

[The MIT License](http://opensource.org/licenses/MIT)
